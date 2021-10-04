# -*- coding: utf-8 -*-
"""olivetti-aneira.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uAPxt-jG32nEAFJUjFW-EytpfD4HfJxe

# Olivetti Faces
"""

import numpy as np
import pandas as pd
import sklearn.decomposition # Módulo donde encontramos el análisis de componentes principales
import sklearn.manifold # Módulo donde encontramos el método t-Distributed Stochastic Neighbor Embedding
import matplotlib.pyplot as plt
import sklearn.datasets
import sklearn.svm # Support vector machines
import sklearn.metrics
import sklearn.gaussian_process # Kernel de transformación del espacio
import sklearn.preprocessing
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import scipy
import sklearn.dummy

"""Olivetti blah blah"""

olivetti_faces = pd.read_csv("olivetti_faces.csv")
olivetti_faces.head()

"""El conjunto de datos contiene ... imágenes y ... atributos (pixeles + etiqueta)"""

olivetti_faces.shape

"""Así se ve el conjunto de datos."""

olivetti_faces.iloc[0,:-1] #row 0 almost complete

fig,axs = plt.subplots(40,10,figsize=(16, 70),subplot_kw={'xticks':[], 'yticks':[]})
for i,ax in enumerate(axs.flat):
    ax.imshow(
         olivetti_faces.iloc[i,:-1].values.reshape(64,-1),
         cmap="gray"
    )

"""Ajustemos un PCA sobre el conjunto de datos."""



pca_olivetti = sklearn.decomposition.PCA()
pca_olivetti.fit(olivetti_faces.iloc[:,:-1])

"""Obtenemos una matriz con 400 componentes."""

pca_olivetti.components_.shape

"""Así se ve el primer componente."""

pca_olivetti.components_[0]

fig,axs = plt.subplots(40,10,figsize=(16, 70),subplot_kw={'xticks':[], 'yticks':[]})
for i,ax in enumerate(axs.flat):
    ax.imshow(
         pca_olivetti.components_[i].reshape(64,-1),
         cmap="gray"
    )

"""Acá podemos ver cuánta varianza explica cada uno de los 64 componentes."""

pca_olivetti.explained_variance_ratio_

"""Visualizamos la suma acumulada de las varianzas explicadas por cada componente."""

plt.plot(
    range(len(pca_olivetti.explained_variance_ratio_)),
    np.cumsum(pca_olivetti.explained_variance_ratio_)
)

"""Ajustemos un PCA de sólo 2 componentes para visualizar el conjunto de datos en un gráfico de dispersión."""

pca_olivetti_2d = sklearn.decomposition.PCA(2)
olivetti_2d=pca_olivetti_2d.fit_transform(olivetti_faces.iloc[:,:-1])
olivetti_2d.shape

"""Cada uno de los números tienden a acumularse juntos"""

plt.scatter(
    olivetti_2d[:,0],
    olivetti_2d[:,1],
    c=olivetti_faces.subject,
    cmap='tab10'
)
plt.colorbar()

fig, axs = plt.subplots(2)

axs[0].imshow(
    olivetti_faces.iloc[0,:-1].values.reshape(64,-1),
    cmap="gray"
)
axs[0].set_title("Original image")

axs[1].imshow(
    pca_olivetti_2d.inverse_transform(olivetti_2d)[0].reshape(64,-1),
    cmap="gray"
)
axs[1].set_title("Image using 2 principal components")
fig.tight_layout()

pca_95p = sklearn.decomposition.PCA(0.95)
olivetti_95p = pca_95p.fit_transform(olivetti_faces.iloc[:,:-1])

pca_95p.components_.shape

fig, axs = plt.subplots(2)

axs[0].imshow(
    olivetti_faces.iloc[0,:-1].values.reshape(64,-1),
    cmap="gray"
)
axs[0].set_title("Imagen original")

axs[1].imshow(
    pca_95p.inverse_transform(olivetti_95p)[0].reshape(64,-1),
    cmap="gray"
)
axs[1].set_title("Imagen utilizando 123 Principal Components")
fig.tight_layout()

"""##Metodo Supervisado: Support Vector Machines"""

(X_train, X_test, y_train, y_test) = sklearn.model_selection.train_test_split(olivetti_faces.iloc[:,:-1].to_numpy(),olivetti_faces.iloc[:,-1:].to_numpy(),test_size=0.3, 
    random_state=11)

# from sklearn.cross_validation import train_test_split

# X_train, X_test, y_train, y_test = train_test_split(
        # faces.data, faces.target, test_size=0.25, random_state=0)

svm_linear = sklearn.svm.SVC(kernel="linear")
svm_linear.fit(X_train, np.ravel(y_train,order='C'))

"""##Cross Validation

"""

olivetti_faces['subject']

"""Funcion copiada del notebook 5.2-cross-validation.ipynb **cross_val_store**():"""

def cross_val_score(**kwargs):
    """
    Recibe los argumentos para pasárselos a la función sklearn.model_selection.cross_validate
    Retorna una lista con los valores de AUCROC de cada una de las divisiones.
    """
    cv = sklearn.model_selection.cross_validate( # Esta función entrena un modelo para distintos subconjuntos generados al azar.
        # scoring = 'roc_auc', # Usamos la medida de AUCROC para medir el rendimiento de los modelos
        cv = sklearn.model_selection.StratifiedKFold( # La división se realiza de manera estratificada
            n_splits = 10, # Creamos 10 subconjuntos
            shuffle = True, # Desordenamos los datos antes de dividirlos
        ),
        n_jobs = None, # Usamos sólo 1 worker para el entrenmiento
        **kwargs # Pasamos los argumentos recibidos por la función
    )
    return cv["test_score"]

dummy_scores = cross_val_score(
    estimator = sklearn.dummy.DummyClassifier(strategy="stratified"),
    X = olivetti_faces.iloc[:,:-1],
    y = olivetti_faces['subject']
)

svm_scores = cross_val_score(
    estimator = sklearn.svm.SVC(),
    X = olivetti_faces.iloc[:,:-1],
    y = olivetti_faces['subject']
)

scores = [ # Guardamos todos los resultados en una lista
    svm_scores,
    dummy_scores
]
names = [
    "Support Vector Machine",
    "Dummy Classifier"
]
plt.boxplot(
    scores,
    labels = names
)
plt.xticks(rotation=45)
plt.show()

dict(
    zip(
        names,
        map(
            np.mean,
            scores
        )
    )
)

"""ANOVA:"""

scipy.stats.f_oneway(*scores)