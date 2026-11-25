# Paper 1 analysis chunk: existing predictions only, no tuning or new inference.
from pathlib import Path
import json, datetime, hashlib, platform, importlib.metadata
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, brier_score_loss
base=Path(__file__).resolve().parent
source_run=base
analysis=base/('analysis_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
analysis.mkdir(exist_ok=False)
figdir=analysis/'figures'; figdir.mkdir()
df=pd.read_csv(source_run/'predictions.csv'); plan=json.loads((source_run/'plan.json').read_text())
assert len(df)==2000 and df.image_id.is_unique
assert (df.predicted_label==(df.cancer_probability>=0.5)).all()
assert np.isfinite(df.cancer_probability).all()
y=df.label.to_numpy().astype(int); p=df.cancer_probability.to_numpy(); q=(p>=0.5).astype(int)
conf=np.maximum(p,1-p); correct=q==y
def stats(y,p):
    q=(p>=0.5).astype(int); c=np.maximum(p,1-p); ok=q==y
    tn,fp,fn,tp=confusion_matrix(y,q,labels=[0,1]).ravel()
    sens=tp/(tp+fn) if tp+fn else np.nan; spec=tn/(tn+fp) if tn+fp else np.nan
    ece=0.
    for lo,hi in zip(np.linspace(0,1,11)[:-1],np.linspace(0,1,11)[1:]):
        mask=(c>=lo)&((c<hi) if hi<1 else (c<=hi))
        if mask.any(): ece+=mask.mean()*abs(ok[mask].mean()-c[mask].mean())
    return {'roc_auc':roc_auc_score(y,p) if len(np.unique(y))==2 else np.nan,'accuracy':ok.mean(),'sensitivity':sens,'specificity':spec,'balanced_accuracy':(sens+spec)/2,'precision':tp/(tp+fp) if tp+fp else np.nan,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else np.nan,'brier':np.mean((p-y)**2),'confidence_ece_10_bins':ece}
point=stats(y,p)
# Patient bootstrap: retain all sampled patches of each drawn patient, including repeats.
patients=sorted(df.patient.unique()); groups=[np.flatnonzero(df.patient.to_numpy()==v) for v in patients]
rng=np.random.default_rng(20261024); boot=[]
for b in range(2000):
    idx=np.concatenate([groups[j] for j in rng.integers(0,len(groups),len(groups))])
    boot.append(stats(y[idx],p[idx]))
boot=pd.DataFrame(boot); boot.to_csv(analysis/'patient_cluster_bootstrap_replicates.csv',index=False)
intervals=[]
for metric,value in point.items():
    values=boot[metric].dropna()
    intervals.append({'metric':metric,'estimate':value,'ci_low':values.quantile(.025),'ci_high':values.quantile(.975),'valid_replicates':len(values),'undefined_replicates':2000-len(values)})
ci=pd.DataFrame(intervals); ci.to_csv(analysis/'metrics_patient_cluster_CI.csv',index=False)
for name in ['patient','slide']:
    table=[]
    for ident,g in df.groupby(name):
        yy=g.label.to_numpy(); pp=g.cancer_probability.to_numpy()
        table.append({name:int(ident),'n':len(g),'positive':int(yy.sum()),'negative':int((yy==0).sum()),**stats(yy,pp)})
    pd.DataFrame(table).to_csv(analysis/(name+'_summary.csv'),index=False)
cohort=df.groupby(['patient','slide']).agg(n=('label','size'),positive=('label','sum')).reset_index()
cohort['negative']=cohort.n-cohort.positive; cohort.to_csv(analysis/'cohort.csv',index=False)
# Reliability of positive-class probability, distinct from confidence ECE above.
reliability=[]
for lo,hi in zip(np.linspace(0,1,11)[:-1],np.linspace(0,1,11)[1:]):
    mask=(p>=lo)&((p<hi) if hi<1 else (p<=hi))
    reliability.append({'lower':lo,'upper':hi,'n':int(mask.sum()),'mean_probability':p[mask].mean() if mask.any() else np.nan,'observed_positive_fraction':y[mask].mean() if mask.any() else np.nan})
rel=pd.DataFrame(reliability); rel.to_csv(analysis/'probability_reliability_bins.csv',index=False)
errors=df.loc[~correct].copy(); errors['error_type']=np.where(errors.label==0,'FP','FN')
errors.sort_values(['confidence','image_id'],ascending=[False,True]).to_csv(analysis/'errors_ranked.csv',index=False)
confidence_summary={'mean_all':float(conf.mean()),'mean_correct':float(conf[correct].mean()),'mean_incorrect':float(conf[~correct].mean()),'errors_ge_90':int(((~correct)&(conf>=.9)).sum()),'errors_ge_95':int(((~correct)&(conf>=.95)).sum()),'n_errors':int((~correct).sum())}
(analysis/'confidence_summary.json').write_text(json.dumps(confidence_summary,indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def savefig(name):
    plt.tight_layout(); plt.savefig(figdir/(name+'.png'),dpi=300,bbox_inches='tight'); plt.savefig(figdir/(name+'.pdf'),bbox_inches='tight'); plt.close()
fpr,tpr,_=roc_curve(y,p)
plt.figure(figsize=(5,4)); plt.plot(fpr,tpr,label=f'AUC = {point["roc_auc"]:.3f}',color='#176b87'); plt.plot([0,1],[0,1],'--',color='grey'); plt.xlabel('False-positive rate'); plt.ylabel('Sensitivity'); plt.legend(); plt.title('Existing-model external discrimination'); savefig('01_ROC')
plt.figure(figsize=(5,4)); plt.plot([0,1],[0,1],'--',color='grey'); plt.plot(rel.mean_probability,rel.observed_positive_fraction,'o-',color='#176b87'); plt.xlabel('Mean predicted cancer probability'); plt.ylabel('Observed positive fraction'); plt.xlim(0,1); plt.ylim(0,1); plt.title('Probability reliability: 10 uniform bins'); savefig('02_calibration')
cm=confusion_matrix(y,q,labels=[0,1]); plt.figure(figsize=(4,4)); plt.imshow(cm,cmap='Blues');
for i in range(2):
    for j in range(2): plt.text(j,i,str(cm[i,j]),ha='center',va='center',fontsize=16,color='white' if cm[i,j]>cm.max()/2 else 'black')
plt.xticks([0,1],['Negative','Positive']); plt.yticks([0,1],['Negative','Positive']); plt.xlabel('Prediction'); plt.ylabel('Reference label'); plt.title('Confusion matrix: threshold 0.50'); savefig('03_confusion')
plt.figure(figsize=(5,4)); plt.hist(conf[correct],bins=np.linspace(.5,1,21),alpha=.65,label='Correct',density=True); plt.hist(conf[~correct],bins=np.linspace(.5,1,21),alpha=.65,label='Incorrect',density=True); plt.xlabel('Predicted-class confidence'); plt.ylabel('Density within outcome group'); plt.legend(); plt.title('Confidence on correct and incorrect predictions'); savefig('04_confidence')
slides=pd.read_csv(analysis/'slide_summary.csv')
fig,ax=plt.subplots(figsize=(7,4)); width=.35; xx=np.arange(len(slides)); ax.bar(xx-width/2,slides.sensitivity,width,label='Sensitivity'); ax.bar(xx+width/2,slides.specificity,width,label='Specificity'); ax.set_xticks(xx,slides.slide.astype(str)); ax.set_ylim(0,1.05); ax.set_xlabel('Slide ID'); ax.set_ylabel('Rate'); ax.legend(); ax.set_title('Slide variation; absent classes yield undefined rates'); savefig('05_slide_rates')
plt.figure(figsize=(7,4)); plt.bar(slides.slide.astype(str),slides.negative,label='Negative'); plt.bar(slides.slide.astype(str),slides.positive,bottom=slides.negative,label='Positive'); plt.xlabel('Slide ID'); plt.ylabel('Sampled patches'); plt.legend(); plt.title('External sample composition by slide'); savefig('06_slide_composition')
versions={k:importlib.metadata.version(k) for k in ['numpy','pandas','scikit-learn','tensorflow','datasets','matplotlib']}
summary={'source_run':str(source_run),'n':len(df),'patients':len(patients),'slides':int(df.slide.nunique()),'positive':int(y.sum()),'negative':int((y==0).sum()),'eligible_metadata_rows':81054,'cluster_bootstrap_replicates':2000,'bootstrap_seed':20261024,'confidence':confidence_summary,'versions':versions,'model_sha256':plan['model_sha256'],'predictions_sha256':hashlib.sha256((source_run/'predictions.csv').read_bytes()).hexdigest(),'status':'exploratory single existing model; prior exposure uncertain; no internal comparison or seed replication'}
(analysis/'analysis_manifest.json').write_text(json.dumps(summary,indent=2))
print('ANALYSIS COMPLETE:',analysis)
print(json.dumps(summary,indent=2)); print(ci.to_string(index=False)); print(slides.to_string(index=False))
