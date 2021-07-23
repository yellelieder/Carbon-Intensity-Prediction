import pandas as pd
    
if __name__=="__main__":
    folder_path=r"Ressources\Downloads\Consumption\Realisierter_Stromverbrauch_"
    ca=folder_path+r"201501010000_201512312359.csv"
    cb=folder_path+r"201601010000_201612312359.csv"
    cc=folder_path+r"201701010000_201712312359.csv"
    cd=folder_path+r"201801010000_201812312359.csv"
    ce=folder_path+r"201901010000_201912312359.csv"
    cf=folder_path+r"202001010000_202012312359.csv"
    cg=folder_path+r"202101010000_202107092359.csv"
    ca_df=pd.read_csv(ca, sep=";")
    cb_df=pd.read_csv(cb, sep=";")
    cc_df=pd.read_csv(cc, sep=";")
    cd_df=pd.read_csv(cd, sep=";")
    ce_df=pd.read_csv(ce, sep=";")
    cf_df=pd.read_csv(cf, sep=";")
    cg_df=pd.read_csv(cg, sep=";")
    ca_df=ca_df.append(cb_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.append(cc_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.append(cd_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.append(ce_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.append(cf_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.append(cg_df, ignore_index=True)
    print(ca_df.size)
    ca_df=ca_df.to_csv(r"Ressources\RawDataMerged\raw_consumption.csv")
    
    folder_path=r"Ressources\Downloads\Production\Realisierte_Erzeugung_"
    pa=folder_path+r"201501010000_201512312359.csv"
    pb=folder_path+r"201601010000_201612312359.csv"
    pc=folder_path+r"201701010000_201712312359.csv"
    ppd=folder_path+r"201801010000_201812312359.csv"
    pe=folder_path+r"201901010000_201912312359.csv"
    pf=folder_path+r"202001010000_202012312359.csv"
    pg=folder_path+r"202101010000_202107092359.csv"
    pa_df=pd.read_csv(pa, sep=";")
    pb_df=pd.read_csv(pb, sep=";")
    pc_df=pd.read_csv(pc, sep=";")
    pd_df=pd.read_csv(ppd, sep=";")
    pe_df=pd.read_csv(pe, sep=";")
    pf_df=pd.read_csv(pf, sep=";")
    pg_df=pd.read_csv(pg, sep=";")
    pa_df=pa_df.append(pb_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.append(pc_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.append(pd_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.append(pe_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.append(pf_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.append(pg_df, ignore_index=True)
    print(pa_df.size)
    pa_df=pa_df.to_csv(r"Ressources\RawDataMerged\raw_production.csv")