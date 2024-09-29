from neo4j import GraphDatabase
import os
from .models import Patient


from dotenv import load_dotenv
from .intent import recognize_intent_with_gpt
load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
#patient = Patient.objects.get(id=1)
def store_entities_in_knowledge_graph(patient, entities):
    with driver.session() as session:
        # Create or match the patient node
        session.run("""
            MERGE (p:Patient {id: $patient_id, name: $patient_name})
            """, patient_id=patient.id, patient_name=f"{patient.first_name} {patient.last_name}")
        
        # Create the first entity node and attach it to the patient
        first_entity_label = list(entities.keys())[0].replace(" ", "_").capitalize()
        first_entity_value = entities[list(entities.keys())[0]]

        # Create or match the first entity node
        session.run(f"""
            MERGE (e:{first_entity_label} {{name: $entity_value}})
            """, entity_value=first_entity_value)

        # Attach the first entity to the patient with a relationship based on the entity type
        session.run(f"""
            MATCH (p:Patient {{id: $patient_id}}), (e:{first_entity_label} {{name: $entity_value}})
            MERGE (p)-[:HAS_{first_entity_label.upper()}]->(e)
            """, patient_id=patient.id, entity_value=first_entity_value)

        # Iterate over the rest of the entities and create relationships dynamically
        previous_entity_label = first_entity_label
        previous_entity_value = first_entity_value

        for entity_type, entity_value in list(entities.items())[1:]:
            entity_label = entity_type.replace(" ", "_").capitalize()

            # Create or match the current entity node
            session.run(f"""
                MERGE (e:{entity_label} {{name: $entity_value}})
                """, entity_value=entity_value)

            # Create a relationship between the previous entity and the current entity
            session.run(f"""
                MATCH (prev:{previous_entity_label} {{name: $prev_value}}), (e:{entity_label} {{name: $entity_value}})
                MERGE (prev)-[:HAS_{entity_label.upper()}]->(e)
                """, prev_value=previous_entity_value, entity_value=entity_value)

            # Update the previous entity to the current one
            previous_entity_label = entity_label
            previous_entity_value = entity_value





def retrieve_information_from_knowledge_graph(patient, user_message):
    keyword = recognize_intent_with_gpt(user_message)

    print(keyword)
    with driver.session() as session:
        # Query to retrieve the information based on the keyword (e.g., "medication")
        result = session.run(f"""
            MATCH (p:Patient {{id: $patient_id}})-[r:HAS_{keyword.upper()}]->(entity)
            OPTIONAL MATCH (entity)-[sub_rel]->(sub_entity)
            RETURN entity.name AS main_entity, sub_entity.name AS related_entity, type(sub_rel) AS relationship_type
            """, patient_id=patient.id)
        
        # Process the results
        information = []
        for record in result:
            main_entity = record["main_entity"]
            related_entity = record.get("related_entity", None)
            relationship_type = record.get("relationship_type", None)

            if related_entity and relationship_type:
                information.append(f"{main_entity} with {relationship_type.replace('HAS_', '').lower()}: {related_entity}")
            else:
                information.append(f"{main_entity}")
        print(information)
        # Return the information as a formatted string
        return "\n".join(information)





driver.close()