import pandas as pd

'''
Own implementon but it seems to be heading towards the anonypy implementation so I might as well just use that one since its more developed.

Keeping this file to potentially work on this more in the future when time permits.
'''
def summarized(partition,dim,quasi_identifers):
    for qi in quasi_identifers:
        partition=partition.sort_values(by=qi)
        if (partition[qi].iloc[0] != partition[qi].iloc[-1]):
            s=f"[{partition[qi].iloc[0]}-{partition[qi].iloc[-1]}]"
        partition[qi]=[s]*partition.size
        

def anonymize(partition, ranks,k,quasi_identifers):
    dim = ranks[0][0]
    
    partition = partition.sort_values(by=dim)
    si = partition[dim].count()
    mid = si//2

    lhs = partition[:mid]
    rhs = partition[mid:]
    
    if (len(lhs)>=k and len(rhs)>=k):
        return pd.concat([anonymize(lhs,ranks,k),anonymize(rhs,ranks,k)])
    
    return summarized(partition,dim,quasi_identifers)

def mondrian(partition, quasi_identifers,k):
    ranks={}
    
    for qi in quasi_identifers:
        ranks[qi] = len(set(partition))
    
    ranks = sorted(ranks.items(), key=lambda t: t[1], reverse=True)

    return anonymize(partition,ranks,k,quasi_identifers)

def k_anon(path_to_file, k, sensitive_value,quasi_identifers):
    data = pd.read_csv(path_to_file)

    result = mondrian(data,quasi_identifers,k,)
    
    print(result)
    #result.to_csv("file_name", index=False)