# Insights de Reviews en Amazon

## Descripción del Proyecto

Este proyecto se centra en aplicar algoritmos de aprendizaje no supervisado a un conjunto de datos de reviews de productos en Amazon para extraer insights de negocio. El dataset fue adquirido durante un evento organizado por la empresa Factored, denominado Datathon. La información relacionada con este evento se encuentra en la carpeta `datathon` de este repositorio. Es importante destacar que todo el contenido dentro de la carpeta `datathon` no forma parte del desarrollo de este proyecto, sino que son presentaciones y códigos externos.

## Preparación de Datos

Debido al gran volumen de datos, estos se cargaron en Google Cloud Storage (GCS) y posteriormente se hicieron accesibles a través de una tabla en BigQuery. Gracias al bono de 300 USD que Google ofrece a los nuevos usuarios, no se incurrió en costos por el uso de servicios en la nube.

- El notebook para cargar los datos a GCS está disponible en `proyecto/upload_dataset_to_gcs.ipynb`.
- Una vez que los datos están en GCS, se pueden utilizar para crear una tabla en BigQuery, tal como se muestra en la documentación.
  
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
  
Los detalles de este procedimiento se encuentran en el notebook `proyecto/proyecto_entrega_1.ipynb`.
