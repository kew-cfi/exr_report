import os
import inspect
import fnmatch
from typing import List, Any
from collections import OrderedDict

path, currentdir = os.path.split(os.path.dirname(inspect.getfile(inspect.currentframe())))


class Config():

    QDEBUG = True

    FILES = dict(
        RAW_DATA = os.path.join("data", "raw"),
        PREPROCESS_DATA = os.path.join("data", "preprocess"),
    )

    ANALYSIS_CONFIG = dict(
        START_DATE      = None, # "2023-05-01"
        END_DATE        = "2023-05-31",
        COUNTRY_LIST    = ["USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", "TRY", "AUD", 
                           "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]
    )

    VARS = OrderedDict(
        EXR = [
            dict(var="KEY",             predictive=False),
            dict(var="FREQ",            predictive=False),
            dict(var="CURRENCY",        predictive=True ),
            dict(var="CURRENCY_DENOM",  predictive=True ),
            dict(var="EXR_TYPE",        predictive=False),
            dict(var="EXR_SUFFIX",      predictive=False),
            dict(var="TIME_PERIOD",     predictive=True ),
            dict(var="OBS_VALUE",       predictive=True ),
            dict(var="OBS_STATUS",      predictive=False),
            dict(var="OBS_CONF",        predictive=False),
            dict(var="OBS_PRE_BREAK",   predictive=False),
            dict(var="OBS_COM",         predictive=False),
            dict(var="TIME_FORMAT",     predictive=False),
            dict(var="BREAKS",          predictive=False),
            dict(var="COLLECTION",      predictive=False),
            dict(var="COMPILING_ORG",   predictive=False),
            dict(var="DISS_ORG",        predictive=False),
            dict(var="DOM_SER_IDS",     predictive=False),
            dict(var="PUBL_ECB",        predictive=False),
            dict(var="PUBL_MU",         predictive=False),
            dict(var="PUBL_PUBLIC",     predictive=False),
            dict(var="UNIT_INDEX_BASE", predictive=False),
            dict(var="COMPILATION",     predictive=False),
            dict(var="COVERAGE",        predictive=False),
            dict(var="DECIMALS",        predictive=False),
            dict(var="NAT_TITLE",       predictive=False),
            dict(var="SOURCE_AGENCY",   predictive=False),
            dict(var="SOURCE_PUB",      predictive=False),
            dict(var="TITLE",           predictive=False),
            dict(var="TITLE_COMPL",     predictive=False),
            dict(var="UNIT",            predictive=False),
            dict(var="UNIT_MULT",       predictive=False),
        ]
    )

    _RENAME_COLUMNS = OrderedDict(
        EXR = {
            "CURRENCY"          : "ORIGIN_CURRENCY",
            "CURRENCY_DENOM"    : "TARGET_CURRENCY",
            "OBS_VALUE"         : "EXCHANGE_RATE",
            "TIME_PERIOD"       : "REPORT_DATE",
        }
    )


    @staticmethod
    def vars(types: List[str]=[], 
            wc_vars: List[str]=[], 
            qreturn_dict: Any=True):
            """ Return list of variable names
            
            Acquire the right features from dataframe to be input into model.  
            Featurs will be acquired based the value "predictive" in the VARS dictionary. 

            Parameters
            ----------
            types : List[str]
                Types of variables to be included based on parent features varible in VARS, 'EXR'.  If empty, all variables will be included.
            wc_vars : List[str]
                Wildcard variables to be included.  If empty, all variables will be included.
            qreturn_dict : Any
                If True, return a list of dictionaries with variable name and other attributes.  If True, return a list of variable names.

            Returns
            -------
            Features with predictive == True in Config.VARS
            """
            if types==None:
                types = [V for V in Config.VARS]
            selected_vars = []
            for t in types:
                for d in Config.VARS[t]:
                    if not d.get("predictive"):
                        continue
                    if len(wc_vars) != 0: 
                        matched_vars = fnmatch.filter(wc_vars, d["var"])
                        if qreturn_dict:
                            for v in matched_vars:
                                dd = d.copy()
                                dd["var"] = v 
                                if not dd in selected_vars:
                                    selected_vars.append(dd)
                        else:
                            for v in matched_vars:
                                if not v in selected_vars:
                                    selected_vars.append(v)
                    else:
                        if qreturn_dict and not d in selected_vars:
                            selected_vars.append(d)
                        else:
                            if not d["var"] in selected_vars:
                                selected_vars.append(d["var"])
            return selected_vars