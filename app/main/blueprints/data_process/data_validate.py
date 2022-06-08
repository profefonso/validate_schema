import pandas as pd
import json
import decimal
from decimal import  Decimal
from pandas_schema import Column, Schema
from pandas_schema.validation import DateFormatValidation, LeadingWhitespaceValidation, TrailingWhitespaceValidation, CanConvertValidation, MatchesPatternValidation, InRangeValidation, InListValidation, CustomElementValidation, CustomSeriesValidation

pd.options.display.max_columns = None
pd.options.display.max_rows = None

class DataValidate():

    def check_decimal(self, dec):
        try:
            Decimal(dec)
        except decimal.InvalidOperation:
            return False
        return True
    
    def check_int(self, num):
        try:
            int(num)
        except ValueError:
            return False
        return True
    
    def check_null(self, val):
        try:
            if pd.isna(val):
                return False
            else:
                return True
        except ValueError:
            return False

    def widths_generate(self,format_type,options):
        int_return = 0
        if "ALPHANUMERIC(" in format_type.upper():
            int_return = format_type.split("(")[1].split(")")[0]
        if "DECIMAL(" in format_type.upper():
            int_return = format_type.split("(")[1].split(")")[0].split(",")[0]
        if "TIMESTAMP" in format_type.upper(): 
            if len(options["format"]) == 26:
                int_return = 24
            if len(options["format"]) == 19:
                int_return = 17
        if "DATE" in format_type.upper():
            int_return = len(options["format"])
        if "NUMERIC SHORT" in format_type.upper():
            int_return = 4

        return int(int_return)


    def read_file(self, path_data, list_widths, columns_name):
        df = pd.read_fwf(
            path_data,
            colspecs="infer",
            header=None,
            widths=list_widths,
        )
        df = df.rename(columns = columns_name)
        return df
    
    def validation_topics(self, field):
        decimal_validation = CustomElementValidation(lambda d: self.check_decimal(d), 'is not decimal')
        int_validation = CustomElementValidation(lambda i: self.check_int(i), 'is not integer')
        null_validation = CustomElementValidation(lambda i: self.check_null(i), 'this field cannot be null')
        list_to_val = [LeadingWhitespaceValidation()]

        try:
            if isinstance(field["type"], list):
                list_type = field["type"]
            else:
                list_type = [field["type"]]

            if "null" not in list_type:
                list_to_val.append(null_validation)
            
            for type_f in list_type:
                if "decimal" in type_f.split("(")[0]:
                    list_to_val.append(decimal_validation)
                
                if ("int32" or "int") in type_f:
                    list_to_val.append(int_validation)
                
                if "date" in type_f:
                    list_to_val.append(DateFormatValidation("%Y-%m-%d"))

        except Exception as e:
            print(e)
        return list_to_val

    
    def read_schema(self, path_data, path_schema):
        list_widths = []
        columns_name = {}
        list_schema_val = []
        data_schema = json.load(open(path_schema))
        colum_number = 0
        for field in data_schema['fields']:
            columns_name[colum_number] = field['name']
            list_valitations = self.validation_topics(field)
            list_schema_val.append(Column(field['name'], list_valitations))
            list_widths.append(self.widths_generate(field['logicalFormat'], field))
            colum_number = colum_number + 1
            
        df = self.read_file(path_data, list_widths, columns_name)
        error_descrip, result_validate = self.validate_schema(df, list_schema_val)
        # data_example = df.head(5).to_csv(index=False).strip('\n').split('\n')
        data_example = df.to_json(orient = 'split')

        return data_example, error_descrip, result_validate

    
    def validate_schema(self, data_f, list_schema_val):
        error_descrip = []
        result_validate = "The file corresponds to the schema!"
        schema = Schema(list_schema_val)
        errors = schema.validate(data_f)

        for error in errors:
            try:
                error_line = {}
                error_text = str(error)
                error_line["row"] = error_text.split("}")[0].split(",")[0].split(":")[1]
                error_line["column"] = error_text.split("}")[0].split(",")[1].split(":")[1]
                error_line["value"] = error_text.split("}")[1].split("\"")[1]
                error_line["description"] = error_text.split("}")[1].split("\"")[2]
                error_descrip.append(error_line)
            except Exception as e:
                pass
            result_validate = "The file contains validation errors!"
            #error_descrip = error_descrip + str(error)
        
        return json.dumps({"data" : error_descrip}), result_validate
