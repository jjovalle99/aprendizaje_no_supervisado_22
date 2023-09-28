# Insights de Reviews en Amazon

## Entrega final
Los resultados de la entrega final pueden ser encontrados en la carpeta `entrega_final`:
- `01_proyecto_final_embeddings_y_analisis_de_sentimiento.ipynb`: Contiene el procedimiento utilizado para realizar el analisis de sentimiento y la obtencion de los embeddings.
- `02_proyecto_final_clusters_y_topicos.ipynb`: Contiene el procedimiento utilizado para hallar los insights de las reseñas (reduccion de dimensionalidad, clusters, obtencion de keywords)
- `utils.py`: Contiene funciones auxiliares para facilitar el desarrollo de los notebooks principales.
- `requirements.txt`: Contiene las liberias utilizadas en el proyecto.

## Descripción del Proyecto

Este proyecto se centra en aplicar algoritmos de aprendizaje no supervisado a un conjunto de datos de reviews de productos en Amazon para extraer insights de negocio. El dataset fue adquirido durante un evento organizado por la empresa Factored, denominado Datathon. La información relacionada con este evento se encuentra en la carpeta `datathon` de este repositorio. Es importante destacar que todo el contenido dentro de la carpeta `datathon` no forma parte del desarrollo de este proyecto, sino que son presentaciones y el codigo utilizado para subir los datos a HuggingFace. Todo el codigo e informacion adicional presente en este repositorio, si representan el desarrollo del proyecto de clase.

## Preparación de Datos

Debido al gran volumen de datos, estos se cargaron en Google Cloud Storage (GCS) y posteriormente se hicieron accesibles a través de una tabla en BigQuery. Gracias al bono de 300 USD que Google ofrece a los nuevos usuarios, no se incurrió en costos por el uso de servicios en la nube.

- El notebook para cargar los datos a GCS está disponible en `proyecto/upload_dataset_to_gcs.ipynb`.
- Una vez que los datos están en GCS, se pueden utilizar para crear una tabla en BigQuery, tal como se muestra a continuación:
<p align="center">
  <img src="https://github.com/jjovalle99/aprendizaje_no_supervisado_22/assets/70274018/b52b5b48-f9c7-4b64-a74a-f34a37edf0a8">
</p>
<p align="center">
  <img src="https://github.com/jjovalle99/aprendizaje_no_supervisado_22/assets/70274018/d99922a6-a0ac-42c5-a1dd-3246369ce3dd">
</p>
<p align="center">
    <img src="https://github.com/jjovalle99/aprendizaje_no_supervisado_22/assets/70274018/51f2c75f-5350-443a-be35-ca807017e4a7">
</p>

  
### Creación de la Tabla Principal en BigQuery

Se utilizó la siguiente consulta SQL para crear la tabla principal que combina las tablas de `metadata` y `reviews`:

```sql
CREATE OR REPLACE TABLE `amazon_reviews.modeling_data` AS 
SELECT 
  TRIM(r.reviewText, " ") as review,
  TRIM(m.brand, " ") as brand,
  m.category.list[OFFSET(0)].item AS first_category_item
FROM 
  `valid-dragon-397303.amazon_reviews.reviews` r
INNER JOIN
  `valid-dragon-397303.amazon_reviews.metadata` m
ON
  r.asin = m.asin
WHERE 
  TRIM(r.reviewText, " ") IS NOT NULL AND
  TRIM(m.brand, " ") IS NOT NULL AND
  ARRAY_LENGTH(m.category.list) > 0
;
```
### Análisis No Supervisado
Para esta primera entrega, el análisis se centrará exclusivamente en la categoría de videojuegos. El flujo de trabajo es el siguiente:

- Generar embeddings utilizando un modelo de lenguaje natural.
- Aplicar una técnica de reducción de dimensionalidad a los embeddings.
- Ejecutar el algoritmo de clustering.
  
Los detalles de este procedimiento se encuentran en el notebook `proyecto/proyecto_entrega_1.ipynb`. Es importante aclarar que, dada la gran cantidad de datos disponibles, haremos uso de GPU (tambien gratis en Google Colab) para todos los procesos en donde sea posible utilizar este hardware. Esto implica que se hara uso de librerias como cuML (en reemplazo de Scikit-Learn) y PyTorch.
