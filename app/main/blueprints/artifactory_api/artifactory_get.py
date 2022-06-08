import os
from artifactory import ArtifactoryPath



class GetArtifactory:

    def get_uuaa(self):
        uuaa_list = []
        try:
            user_name_api = os.environ.get('USER_NAME_ARTIFACTORY')
            api_key = os.environ.get('API_KEY_ARTIFACTORY')

            path = ArtifactoryPath(
                "https://globaldevtools.bbva.com/artifactory/da-datio-dev/schemas/co/", 
                auth=(user_name_api, api_key),
            )

            for uuaa_line in path:
                uuaa_name = str(uuaa_line).split("/")[-1]
                uuaa_list.append(uuaa_name)
        except Exception as e:
            print(e)
            uuaa_list.append("Error to get UUAA List")
        
        return uuaa_list

    def get_table_uuaa(self,uuaa):
        table_list = []
        try:
            user_name_api = os.environ.get('USER_NAME_ARTIFACTORY')
            api_key = os.environ.get('API_KEY_ARTIFACTORY')

            path = ArtifactoryPath(
                f"https://globaldevtools.bbva.com/artifactory/da-datio-dev/schemas/co/{uuaa}/raw/", 
                auth=(user_name_api, api_key),
            )

            for table_line in path:
                table_name = str(table_line).split("/")[-1]
                table_list.append(table_name)
        except Exception as e:
            print(e)
            table_list.append("Error to get Tables lIST for UUAA")
        
        return table_list

    
    def get_schema_table_uuaa(self, uuaa, table, env_table, path_save):
        try:
            user_name_api = os.environ.get('USER_NAME_ARTIFACTORY')
            api_key = os.environ.get('API_KEY_ARTIFACTORY')

            path = ArtifactoryPath(
                f"https://globaldevtools.bbva.com/artifactory/da-datio-dev/schemas/co/{uuaa}/{env_table}/{table}/latest/{table}.output.schema", 
                auth=(user_name_api, api_key),
            )

            name_schema_download = f"{table}.output.schema"

            path.writeto(out=f"{path_save}/{name_schema_download}")

            return name_schema_download

        except Exception as e:
            print(e)
        
            return ""
