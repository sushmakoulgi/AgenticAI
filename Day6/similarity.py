import numpy as np

def cosine_similarity(vector1,vector2):
    vector1_array=np.array(vector1)
    vector2_array=np.array(vector2)

    prod=np.dot(vector1_array,vector2_array)

    return prod/(np.linalg.norm(vector1_array)* np.linalg.norm(vector2_array))



