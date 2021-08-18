# region Import libraries  ####################################################################################

from requests.packages.urllib3 import connection_from_url
import streamlit as st
import os
import json
import math  # (for rounding up)

import requests
from bs4 import BeautifulSoup

import urllib3
import pandas as pd
import tempfile
import os

# import base64
import matplotlib as plt
import seaborn as sns

# from annotated_text import annotated_text

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# from google.cloud import language_v1
from google.cloud.language_v1 import enums


# For Download button (Johannes)
from functionforDownloadButtons import download_button
import os
import json

# import base64
# import json


st.set_option("deprecation.showfileUploaderEncoding", False)

# endregion Import libraries  ####################################################################################

# region Layout size ####################################################################################


def _max_width_():
    max_width_str = f"max-width: 1550px;"
    # max_width_str = f"max-width: 1550px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()

# endregion Layout size ####################################################################################

# region Top area ############################################################

# Using the "with" syntax

# urlONEnotFIVE = "initialised"

st.image("logo.png", width=785)

c1, c2, c3, c4 = st.columns(4)

# st.header("")

# with st.expander("📝 - To-Do's - Roadmap NOW ", expanded=True):
#    st.write(
#        """
# - [OTHER ISSUES]
# - See if Advertools can scrape data for 'https://www.tatielou.co.uk/'
# - Top 15 doesn't seem to be working - retrieves 30
# - Add A CATCH-ALL ERROR when pasted URLs are 404s "MaxRetryError: try with http://tatielo.co.uk/"
# - Add a button to catch no data error: "TypeError: reduce() of empty sequence with no initial value"
#
# - [ERRORS TO FIX! Can wait - caveat to client]
# - [error #01] Add if URL list  2? - 1 URL only doesn't work - need a specific message for that error
# - [error #02] Do a catch expection for Error if no PPC DATA - i.e. with 2 client-side rendered URLs "https://www.tatielou.co.uk/" and "https://www.tatielou.co.uk/pages/contact-us"
# - [error #02] ValueError: You are trying to merge on object and float64 columns. If you wish to proceed you should use pd.concat
#
# - [FORMATTING ISSUES]
# - Add "check results" header
# - Add Emoji + title tag
# - Add top header: done by Charly wargnier - contact: add email address
# - Associate keys/values from KeywordsEverywhere country dictionnary - See what's been done on Suganthan's app with the separate "countries" file
# - Add a special error box for when forgetting to poad credentials "NameError: name 'client' is not defined"
# - Add tooltips (e.g. for languages)
# - Fix percentage issue in table
# - Fix formatting in master section
# - Fix black marks in nan section in tables
#
# - [CHECK BUGS]
#
# - [UNTESTED BUGS]
# - Check CSV names for each download button
# - Try to paste blank lines in boxes
# - (DOESN'T WORK!) Test with 1 URL
# - Check what's happening when more than 5 URLs are pasted
# - Check what's happening when URLs with parentheses is pasted
# - Try with URLs given by the client (see Slack)
# - Try to paste duplicated URLs
# - Try to launch API call with an empty field
# - Try with other URLs
#
#
# """
#    )
#
#    st.header("")
#
# with st.expander("📝 - Done", expanded=False):
#    st.write(
#        """
# - [TESTED BUGS]
# - (SEEMS TO BE WORKING) Test with 2 URLs
# - (SEEMS TO BE WORKING) Test with 3 URLs
# - (SEEMS TO BE WORKING) Test with 4 URLs
# - (SEEMS TO BE WORKING) Test with 5 URLs
#
# - NO AS CONFUSING - Add more languages to Google NLP
# - Add the KeywordEverywhere's global setting in location dropdown  (raised by Eric)
# - Fix error when adding less than 5 URLs
# - Add a series of sections which would show entities present in URL #01 yet not in other URLs (namely, URLs #02 to #05)  (raised by Jorge)
# - Add [*Named Entity Recognition*](https://en.wikipedia.org/wiki/Named-entity_recognition) for each retrieved entity
# - Enable entity analysis in bulk
#
# """
#    )
#
#    st.header("")
#
# with st.expander("📝 - To-Do's - LATER", expanded=False):
#    st.write(
#        """
# - Add character count for each URL
# - Add a way to display scraped content
# - Add viz?
# - Add a button to catch no data error: "TypeError: reduce() of empty sequence with no initial value"
# - Add Selenium - Client side rendering?
# - Remove URLLib library/ replace with advertools - Discussion with Elias: https://bit.ly/3ffI1SG
# - Very long articles (like [this one](https://en.wikipedia.org/wiki/COVID-19_pandemic_cases)) do not work work. I'm on it! :)
# - Add basic *Cost Estimator*?
# - Add *salience difference* in the main table?
#
# """
#    )
#
#    st.header("")


with c3:
    st.write("")

# region Tooltips ############################################################

tooltip_Googlecredentials = """
            
**How to find your credentails **:

- TBC
- TBC

More details on [Google's website](https://cloud.google.com/natural-language/docs/languages)

"""

tooltip_GoogleNLP = """
            
**Available Countries with KWEverywhere**:

- English:	en
- French:	fr
- Spanish:	es
- Italian:	it
- Portuguese: (Brazilian & Continental)	pt
- German:	de
- Chinese: (Simplified)	zh
- Chinese: (Traditional)	zh-Hant
- Japanese:	ja
- Korean:	ko
- Russian:	ru

More details on [Google's website](https://cloud.google.com/natural-language/docs/languages)

"""

tooltip_Countries = """
            
**Available Countries with KWEverywhere**:

    - "": "Global",
    - "au": "Australia",
    - "ca": "Canada",
    - "in": "India",
    - "nz": "New Zealand",
    - "za": "South Africa",
    - "uk": "United Kingdom",
    - "us": "United States",

More details on the [KeywordsEverywhere website](https://api.keywordseverywhere.com/docs/#/keywords/get_countries)

"""

# endregion Tooltips ############################################################


@st.cache(allow_output_mutation=True, show_spinner=False)
def sample_analyze_entities(html_content):
    # client = language_v1.LanguageServiceClient()
    # Available types: PLAIN_TEXT, HTML
    type_ = (
        enums.Document.Type.HTML
    )  # you can change this to be just text; doesn't have to be HTML.
    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages

    language = languageDropdown
    # language = "en"
    document = {"content": html_content, "type": type_, "language": language}
    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    return response


# Cache doesn't work
# @st.cache(allow_output_mutation=True)
def return_entity_dataframe(response):
    output = sample_analyze_entities(response.data)
    output_list = []
    for entity in output.entities:
        entity_dict = {}
        entity_dict["Entity Name"] = entity.name
        entity_dict["Entity Type"] = enums.Entity.Type(entity.type).name
        entity_dict["Salience (" + response._request_url + ")"] = entity.salience
        entity_dict["Ent. Count (" + response._request_url + ")"] = len(entity.mentions)
        output_list.append(entity_dict)
    json_entity_analysis = json.dumps(output_list)

    from io import StringIO

    # newdf = pd.read_json(StringIO(temp))
    # df = pd.read_json(json_entity_analysis)
    df = pd.read_json(StringIO(json_entity_analysis))
    # summed_df = df.groupby(["Entity Name"]).sum()
    # summed_df.sort_values(
    #    by=["Salience (" + response._request_url + ")"], ascending=False
    # )
    # df1 = df.groupby(["entity_name", "entity_type"]).sum().reset_index()
    df1 = df.groupby(["Entity Name", "Entity Type"]).sum().reset_index()
    return df1


# endregion NLP functions ###################################################################################

st.header("")

st.markdown("## **🔑 Settings **")  #########

with st.expander("↕️ Toggle Settings pane ", expanded=True):

    st.markdown("### **① Upload your Google Cloud NLP credentials **")  #########
    c3, c4, c5 = st.columns([1.5, 4, 1.5])

    with c4:
        try:
            uploaded_file = st.file_uploader("", type="json")
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(uploaded_file.getvalue())
            try:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = fp.name
                with open(fp.name, "rb") as a:
                    client = language.LanguageServiceClient.from_service_account_json(
                        fp.name
                    )

            finally:
                if os.path.isfile(fp.name):
                    os.unlink(fp.name)

        except AttributeError:

            print("wait")

    # with c4:
    #    st.markdown("####")
    #    #st.text("")
    #    c = st.container()
    #    if uploaded_file:
    #        st.success("✅ Your Google NLP credentials have been uploaded!")

    from urllib.request import urlopen, Request

    user_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    http = urllib3.PoolManager(headers=headers)
    # http = urllib3.PoolManager()

    # http = urllib3.PoolManager()
    # http = urllib3.PoolManager()

    listOne = [
        "https://octopus.mx/",
        "https://www.charlywargnier.com",
        "https://www.tatielou.co.uk/pages/contact-us",
        "https://www.tatielou.co.uk/",
        "https://www.tatielou.co.uk/pages/about-us",
    ]

    # listOne

    # with st.expander("📝 - languageDropdown ", expanded=False):

    st.markdown("### **② Choose language and location settings **")

    c3, c4, c5 = st.columns([3, 0.1, 3])

    # c10, c20 = st.columns(2)

    with c3:

        # with st.form(key="my_form"):
        # text_input = st.text_input(label="Enter some text")
        languageDropdown = st.selectbox(
            "Select the language for entity analysis",
            ["es", "en", "fr"],
            help=tooltip_GoogleNLP,
        )

    with c5:

        PPCLocation = st.selectbox(
            "Select the Keywords Everywhere Country",
            ["Global", "au", "ca", "in", "nz", "za", "uk", "us"],
            help=tooltip_Countries,
        )
        # submit_button = st.form_submit_button(label="Submit")

    st.markdown("### **③  Paste the URLs you want to analyse **")

    MAX_LINES = 5

    # st.markdown("### **① Upload your Google Cloud NLP credentials **")  #########
    # c3, c4, c5 = st.columns([1, 3, 1])

    text = st.text_area("One URL per line (5 max)", height=120, key="1")
    lines = text.split("\n")  # A list of lines
    if len(lines) > MAX_LINES:
        st.warning(f"🐙 Heads-up! Only the first {MAX_LINES} URLs will be processed!")
        lines = lines[:MAX_LINES]
    linesList = []
    for x in lines:
        linesList.append(x)
    linesList = list(dict.fromkeys(linesList))  # Remove dupes
    linesList = list(filter(None, linesList))  # Remove empty

    start_execution = st.button(" Run model! ✨ ")

    if text and start_execution:
        pass
    elif text and not start_execution:
        pass
    elif not text and not start_execution:
        st.stop()
    else:
        pass

result = []

st.markdown("## **✨ Check results  **")

st.markdown("### ** ⭕ Top 15 section (entites in #01 but not in other URLs)  **")

for x in linesList:
    result.append(return_entity_dataframe(http.request("GET", x)))

from functools import reduce

# create a global merge (merging all results together!)
df_merged = reduce(
    lambda left, right: pd.merge(
        left, right, on=["Entity Name", "Entity Type"], how="outer"
    ),
    result,
)

afinal = list(df_merged)
# len(afinal)
##################

b = [
    "Entity Name",
    "Entity Type",
    "Salience URL #01",
    "Ent. Count URL #01",
    "Salience URL #02",
    "Ent. Count URL #02",
    "Salience URL #03",
    "Ent. Count URL #03",
    "Salience URL #04",
    "Ent. Count URL #04",
    "Salience URL #05",
    "Ent. Count URL #05",
]

listTruncated = b[0 : len(afinal)]
# listTruncated
df_merged.columns = listTruncated

df_merged3 = df_merged.head(3)
testList = df_merged3["Entity Name"].to_list()

# region [Set-up] ALL SUB LISTs   ####################################################################################

# region IN ONE BUT NOT OTHERS  ####################################################################################

# region urlONEnotTWO   ####################################################################################

urlONEnotTWO = (
    # Select only columns for URL 01 and 02
    df_merged.iloc[:, 0:6][df_merged["Salience URL #02"].isna()]
    .dropna(subset=["Salience URL #01"])
    .sort_values(by=df_merged.columns[2], ascending=False)
    .reset_index(drop=True)
    # df = df.reset_index(drop=True)
    .head(10)
)

ListinONEnotTWO = urlONEnotTWO["Entity Name"].to_list()


# endregion urlONEnotTWO   ####################################################################################

# region urlONEnotTHREE   ####################################################################################

if len(linesList) > 2:

    urlONEnotTHREE = (
        # Select only columns for URL 01 and 02
        df_merged.iloc[:, [0, 1, 2, 3, 6, 7]][df_merged["Salience URL #03"].isna()]
        .dropna(subset=["Salience URL #01"])
        .sort_values(by=df_merged.columns[2], ascending=False)
        .reset_index(drop=True)
        # df = df.reset_index(drop=True)
        .head(10)
    )

    ListinONEnotTHREE = urlONEnotTHREE["Entity Name"].to_list()

else:
    # "false"
    pass


# endregion urlONEnotTHREE   ####################################################################################

# region urlONEnotFOUR   ####################################################################################

if len(linesList) > 3:

    urlONEnotFOUR = (
        df_merged.iloc[:, [0, 1, 2, 3, 8, 9]][df_merged["Salience URL #04"].isna()]
        .dropna(subset=["Salience URL #01"])
        .sort_values(by=df_merged.columns[2], ascending=False)
        .reset_index(drop=True)
        .head(10)
    )

    ListinONEnotFOUR = urlONEnotFOUR["Entity Name"].to_list()

else:
    pass

# endregion urlONEnotFOUR   ####################################################################################

# region urlONEnotFIVE   ####################################################################################

if len(linesList) > 4:

    urlONEnotFIVE = (
        # Select only columns for URL 01 and 02
        # df_merged.iloc[:, 0:6][df_merged["Salience URL #03"].isna()]
        df_merged.iloc[:, [0, 1, 2, 3, 10, 11]][df_merged["Salience URL #05"].isna()]
        .dropna(subset=["Salience URL #01"])
        .sort_values(by=df_merged.columns[2], ascending=False)
        .reset_index(drop=True)
        # df = df.reset_index(drop=True)
        .head(10)
    )

    ListinONEnotFIVE = urlONEnotFIVE["Entity Name"].to_list()

else:
    pass


ListinONE = []
try:

    if ListinONEnotTWO:
        ListinONE.append(ListinONEnotTWO)
    if ListinONEnotTHREE:
        ListinONE.append(ListinONEnotTHREE)
    if ListinONEnotFOUR:
        ListinONE.append(ListinONEnotFOUR)
    if ListinONEnotFIVE:
        ListinONE.append(ListinONEnotFIVE)
    else:
        pass

except NameError as err:
    pass


# endregion urlONEnotFIVE   ####################################################################################

# endregion IN ONE BUT NOT OTHERS  ####################################################################################

# region IN OTHERS BUT NOT ONE   ####################################################################################

# region urlTWOnotONE   ####################################################################################

urlTWOnotONE = (
    # Select only columns for URL 01 and 02
    df_merged.iloc[:, 0:6][df_merged["Salience URL #01"].isna()]
    .dropna(subset=["Salience URL #02"])
    .sort_values(by=df_merged.columns[4], ascending=False)
    .reset_index(drop=True)
    # df = df.reset_index(drop=True)
    .head(10)
)

ListurlTWOnotONE = urlTWOnotONE["Entity Name"].to_list()

# st.header("urlTWOnotONE")
# st.table(urlTWOnotONE)

# endregion urlTWOnotONE   ####################################################################################

# region urlTHREEnotONE   ####################################################################################

if len(linesList) > 2:

    urlTHREEnotONE = (
        # Select only columns for URL 01 and 02=3
        df_merged.iloc[:, [0, 1, 2, 3, 6, 7]][df_merged["Salience URL #01"].isna()]
        .dropna(subset=["Salience URL #03"])
        .sort_values(by=df_merged.columns[6], ascending=False)
        .head(10)
    )

    ListurlTHREEnotONE = urlTHREEnotONE["Entity Name"].to_list()

else:
    # "false"
    pass

# "ListurlTHREEnotONE"
# ListurlTHREEnotONE

# endregion urlTHREEnotONE   ####################################################################################

# region urlFOURnotONE   ####################################################################################

if len(linesList) > 3:

    urlFOURnotONE = (
        df_merged.iloc[:, [0, 1, 2, 3, 8, 9]][df_merged["Salience URL #01"].isna()]
        # df[df['column name'].isnull()]
        # df[df['column name'].isnull()]
        # .isna(subset=["Salience URL #01"])
        .dropna(subset=["Salience URL #04"])
        .sort_values(by=df_merged.columns[8], ascending=False)
        .reset_index(drop=True)
        .head(10)
    )

    ListurlFOURnotONE = urlFOURnotONE["Entity Name"].to_list()

else:
    pass

# endregion urlFOURnotONE ####################################################################################

# region urlFIVEnotONE ####################################################################################

if len(linesList) > 4:

    urlFIVEnotONE = (
        df_merged.iloc[:, [0, 1, 2, 3, 10, 11]][df_merged["Salience URL #01"].isna()]
        .dropna(subset=["Salience URL #05"])
        .sort_values(by=df_merged.columns[10], ascending=False)
        .reset_index(drop=True)
        .head(10)
    )

    ListurlFIVEnotONE = urlFIVEnotONE["Entity Name"].to_list()

else:
    pass


# endregion urlFIVEnotONE   ####################################################################################

# endregion IN OTHERS BUT NOT ONE   ####################################################################################

# endregion [Set-up] ALL SUB LISTs   ####################################################################################


# region [MASTER] Keywords Everywhere  ####################################################################################

# region Build list for Keywords Everywhere ####################################################################################

# region ALL LISTS IN URL ONE ####################################################################################

# ListinONE

#######################
# ListinONE = ListinONEnotTWO + ListinONEnotTHREE + ListinONEnotFOUR + ListinONEnotFIVE
#######################

# ListinONE

# endregion ALL LISTS IN URL ONE ####################################################################################

# region ALL LISTS *** NOT *** IN URL ONE ####################################################################################

# st.stop()

ListNOTinONE = []

try:

    if ListurlTWOnotONE:
        ListNOTinONE.append(ListurlTWOnotONE)
    if ListurlTHREEnotONE:
        ListNOTinONE.append(ListurlTHREEnotONE)
    if ListurlFOURnotONE:
        ListNOTinONE.append(ListurlFOURnotONE)
    if ListurlFIVEnotONE:
        ListNOTinONE.append(ListurlFIVEnotONE)
    else:
        pass

except NameError as err:
    pass

# ListNOTinONE

# ListNOTinONE = (
#    ListurlTWOnotONE + ListurlTHREEnotONE + ListurlFOURnotONE + ListurlFIVEnotONE
# )

# ListNOTinONE

# endregion ALL LISTS *** NOT *** IN URL ONE ####################################################################################

# region ALL LISTS  ####################################################################################

from itertools import chain

# print(list(chain(*testListAll)))

# list(chain(*ListinONE))
# list(chain(*ListNOTinONE))

# "Chain_ListinONE"
# st.write(list(chain(*ListinONE)))
# "Chain_ListNOTinONE"
# st.write(list(chain(*ListNOTinONE)))

ListinONE = list(chain(*ListinONE))
ListNOTinONE = list(chain(*ListNOTinONE))


testListAll = ListinONE + ListNOTinONE
# testListAll = list(dict.fromkeys(ListinONE + ListNOTinONE))


# My_list=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 5, 8, 11, 6, 4, 8, 1, 2, 7, 1]]
# print(list(chain(*My_list)))

# "ListNOTinONE"
# ListNOTinONE
#
# "ListinONE"
# ListinONE
#
# "testListAll"
# testListAll


# "testListAll"
# testListAll

# endregion ALL LISTS  ####################################################################################

# endregion Build list for Keywords Everywhere ####################################################################################

# region [Set-up] Keywords Everywhere ####################################################################################

API_KEY = "f7adbad4454c7e31b5fc"

# Define the parameters
my_data = {
    "country": PPCLocation,
    # Mexican Pesos
    "currency": "mxn",
    #'currency': 'USD',
    "dataSource": "gkp",
    #'kw[]': ["keywords tool","SEO"]
    # "kw[]": testList,
    "kw[]": testListAll,
}

my_headers = {
    "Accept": "application/json",
    #'Authorization': 'Bearer <YOUR_API_KEY>'
    "Authorization": "Bearer " + API_KEY,
}

response = requests.post(
    "https://api.keywordseverywhere.com/v1/get_keyword_data",
    data=my_data,
    headers=my_headers,
)

# response.json()
JSONall = response.json()
type(response.json())
# JSONall
DATAOnly = JSONall["data"]

# Create a list with search volumes
Search_Volume = []
for i in DATAOnly:
    Search_Volume.append(i["vol"])
    # Search_Volume.append(i["trend"][1]["value"])

# Search_Volume
# Create a list with competition data

CompetitionData = []
for i in DATAOnly:
    CompetitionData.append(i["competition"])

#############################

# st.write(len(testListAll))
# st.write(len(Search_Volume))
# st.write(len(CompetitionData))

#############################

# st.stop()

# Join list with initial dataframe that contains keywords
joinedList = pd.DataFrame(
    {
        "Entity Name": testListAll,
        "Search Volume": Search_Volume,
        "Competition": CompetitionData,
    }
    # {"keyword": testList, "competition": CompetitionData}
)


# joinedList

# endregion Set up Keywords Everywhere  ####################################################################################

# endregion Keywords Everywhere MASTER ####################################################################################

# region Format dictionary +Tables   ####################################################################################

# region Format dictionary  ####################################################################################

format_dictionary = {
    "Search Volume": "{:,}",
    "Competition": "{:.1%}",
    "Ent. Count URL #01": "{:.0f}",
    "Ent. Count URL #02": "{:.0f}",
    "Ent. Count URL #03": "{:.0f}",
    "Ent. Count URL #04": "{:.0f}",
    "Ent. Count URL #05": "{:.0f}",
    "Salience URL #01": "{:.1%}",
    "Salience URL #02": "{:.1%}",
    "Salience URL #03": "{:.1%}",
    "Salience URL #04": "{:.1%}",
    "Salience URL #05": "{:.1%}",
}

# endregion Format dictionary ####################################################################################

# region Column names ####################################################################################

column_names01_02 = [
    "Entity Name",
    "Entity Type",
    "Search Volume",
    "Competition",
    "Salience URL #01",
    "Ent. Count URL #01",
    "Salience URL #02",
    "Ent. Count URL #02",
]

column_names01_03 = [
    "Entity Name",
    "Entity Type",
    "Search Volume",
    "Competition",
    "Salience URL #01",
    "Ent. Count URL #01",
    "Salience URL #03",
    "Ent. Count URL #03",
]

column_names01_04 = [
    "Entity Name",
    "Entity Type",
    "Search Volume",
    "Competition",
    "Salience URL #01",
    "Ent. Count URL #01",
    "Salience URL #04",
    "Ent. Count URL #04",
]

column_names01_05 = [
    "Entity Name",
    "Entity Type",
    "Search Volume",
    "Competition",
    "Salience URL #01",
    "Ent. Count URL #01",
    "Salience URL #05",
    "Ent. Count URL #05",
]

# endregion ALL COLUMN NAMES ####################################################################################

# endregion Format dictionary +Tables   ####################################################################################

#############################

# region [CSV_Button] ALL SUB LISTs   ####################################################################################

# region [CSV_Button] IN ONE BUT NOT OTHERS  ####################################################################################

# region [CSV_Button] urlONEnotTWO ####################################################################################

with st.expander("⯈ Top 15 entities - In #01 NOT #02", expanded=False):

    st.markdown("")

    #  Merge data (google NLP + Keyword Everywhere)
    inner_joinONEnotTWO = pd.merge(
        urlONEnotTWO, joinedList, on="Entity Name", how="inner"
    )

    # Remove old index + re-index table
    inner_joinONEnotTWO = inner_joinONEnotTWO.reindex(columns=column_names01_02)

    # Add styling
    cmGreen = sns.light_palette("green", as_cmap=True)
    cmRed = sns.light_palette("red", as_cmap=True)
    inner_joinONEnotTWOStyled = inner_joinONEnotTWO.style.background_gradient(
        cmap=cmGreen,
        subset=[
            "Search Volume",
            "Salience URL #01",
            "Salience URL #02",
            "Ent. Count URL #01",
            "Ent. Count URL #02",
        ],
    ).background_gradient(
        cmap=cmRed,
        subset=[
            "Competition",
        ],
    )

    # Format as per format_dictionary
    inner_joinONEnotTWOStyled = inner_joinONEnotTWOStyled.format(format_dictionary)

    CSVButton2 = download_button(inner_joinONEnotTWO, "Model2.csv", "Download CSV")
    st.table(inner_joinONEnotTWOStyled)

# endregion [CSV_Button] urlONEnotTWO ####################################################################################

# region [CSV_Button] urlONEnotTHREE ####################################################################################

if len(linesList) > 2:

    with st.expander("⯈ Top 15 entities - In #01 NOT #03", expanded=False):

        st.markdown("")

        #  Merge data (google NLP + Keyword Everywhere)
        inner_joinONEnotTHREE = pd.merge(
            urlONEnotTHREE, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_joinONEnotTHREE = inner_joinONEnotTHREE.reindex(columns=column_names01_02)

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_joinONEnotTHREEStyled = inner_joinONEnotTHREE.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #02",
                "Ent. Count URL #01",
                "Ent. Count URL #02",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_joinONEnotTHREEStyled = inner_joinONEnotTHREEStyled.format(
            format_dictionary
        )

        CSVButton2 = download_button(
            inner_joinONEnotTHREE, "Model2.csv", "Download CSV"
        )
        st.table(inner_joinONEnotTHREEStyled)

else:
    pass

# endregion [CSV_Button] urlONEnotTHREE ####################################################################################

# region [CSV_Button] urlONEnotFOUR ####################################################################################

if len(linesList) > 3:

    with st.expander("⯈ Top 15 entities - In #01 NOT #04", expanded=False):

        st.markdown("")

        #  Merge data (google NLP + Keyword Everywhere)
        inner_joinONEnotFOUR = pd.merge(
            urlONEnotFOUR, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_joinONEnotFOUR = inner_joinONEnotFOUR.reindex(columns=column_names01_02)

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_joinONEnotFOURStyled = inner_joinONEnotFOUR.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #02",
                "Ent. Count URL #01",
                "Ent. Count URL #02",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_joinONEnotFOURStyled = inner_joinONEnotFOURStyled.format(
            format_dictionary
        )

        CSVButton2 = download_button(inner_joinONEnotFOUR, "Model2.csv", "Download CSV")
        st.table(inner_joinONEnotFOURStyled)
else:
    pass

# endregion [CSV_Button] urlONEnotFOUR ####################################################################################

# region [CSV_Button] urlONEnotFIVE ####################################################################################

# if urlONEnotFIVE == "initialised":

if len(linesList) > 4:

    with st.expander("⯈ Top 15 entities - In #01 NOT #05", expanded=False):

        st.markdown("")

        #  Merge data (google NLP + Keyword Everywhere)
        inner_joinONEnotFIVE = pd.merge(
            urlONEnotFIVE, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_joinONEnotFIVE = inner_joinONEnotFIVE.reindex(columns=column_names01_02)

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_joinONEnotFIVEStyled = inner_joinONEnotFIVE.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #02",
                "Ent. Count URL #01",
                "Ent. Count URL #02",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_joinONEnotFIVEStyled = inner_joinONEnotFIVEStyled.format(
            format_dictionary
        )

        CSVButton2 = download_button(inner_joinONEnotFIVE, "Model2.csv", "Download CSV")
        st.table(inner_joinONEnotFIVEStyled)

else:
    pass

# endregion [CSV_Button] urlONEnotFIVE ####################################################################################


# endregion IN ONE BUT NOT OTHERS  ####################################################################################

# region [CSV_Button] IN OTHERS but not in ONE  ####################################################################################

st.markdown("### ** ⭕ Top 15 section (entites in other URLs but not in #01) **")

# region [CSV_Button] urlTWOnotONE ####################################################################################

st.markdown("")

with st.expander("⯈ Top 15 entities - In #02 NOT #01", expanded=False):

    st.markdown("")

    #  Merge data (google NLP + Keyword Everywhere)
    inner_joinTWOnotONE = pd.merge(
        urlTWOnotONE, joinedList, on="Entity Name", how="inner"
    )

    # Remove old index + re-index table
    inner_joinTWOnotONE = inner_joinTWOnotONE.reindex(columns=column_names01_02)

    # Add styling
    cmGreen = sns.light_palette("green", as_cmap=True)
    cmRed = sns.light_palette("red", as_cmap=True)
    inner_joinTWOnotONEStyled = inner_joinTWOnotONE.style.background_gradient(
        cmap=cmGreen,
        subset=[
            "Search Volume",
            "Salience URL #01",
            "Salience URL #02",
            "Ent. Count URL #01",
            "Ent. Count URL #02",
        ],
    ).background_gradient(
        cmap=cmRed,
        subset=[
            "Competition",
        ],
    )

    # Format as per format_dictionary
    inner_joinTWOnotONEStyled = inner_joinTWOnotONEStyled.format(format_dictionary)

    CSVButton2 = download_button(inner_joinTWOnotONE, "Model2.csv", "Download CSV")
    st.table(inner_joinTWOnotONEStyled)


# endregion urlTWOnotONE ####################################################################################

# region [CSV_Button] urlTHREEnotONE ####################################################################################

if len(linesList) > 2:

    with st.expander("⯈ Top 15 entities - In #03 NOT #01", expanded=False):

        st.markdown("")

        inner_jointTHREEnotONE = pd.merge(
            urlTHREEnotONE, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_jointTHREEnotONE = inner_jointTHREEnotONE.reindex(
            columns=column_names01_03
        )

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_jointTHREEnotONEStyled = inner_jointTHREEnotONE.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #03",
                "Ent. Count URL #01",
                "Ent. Count URL #03",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_jointTHREEnotONEStyled = inner_jointTHREEnotONEStyled.format(
            format_dictionary
        )

        CSVButton3 = download_button(
            inner_jointTHREEnotONE, "Model3.csv", "Download CSV"
        )
        st.table(inner_jointTHREEnotONEStyled)

        #############################

else:
    pass

# endregion urlTHREEnotONE ####################################################################################

# region [CSV_Button] urlFOURnotONE ####################################################################################

if len(linesList) > 3:

    with st.expander("⯈ Top 15 entities - In #04 NOT #01", expanded=False):

        st.markdown("")

        inner_joinOneAndFour = pd.merge(
            urlFOURnotONE, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_joinOneAndFour = inner_joinOneAndFour.reindex(columns=column_names01_04)

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_joinOneAndFourStyled = inner_joinOneAndFour.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #04",
                "Ent. Count URL #01",
                "Ent. Count URL #04",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_joinOneAndFourStyled = inner_joinOneAndFourStyled.format(
            format_dictionary
        )

        CSVButton4 = download_button(inner_joinOneAndFour, "Model4.csv", "Download CSV")
        st.table(inner_joinOneAndFourStyled)

else:
    pass

# endregion urlFOURnotONE ####################################################################################

# region [CSV_Button] urlFIVEnotONE ####################################################################################

if len(linesList) > 4:

    with st.expander("⯈ Top 15 entities - In #05 NOT #01", expanded=False):

        st.markdown("")

        # lenlinesList = len(linesList)
        # lenlinesList

        inner_joinOneAndFive = pd.merge(
            urlFIVEnotONE, joinedList, on="Entity Name", how="inner"
        )

        # Remove old index + re-index table
        inner_joinOneAndFive = inner_joinOneAndFive.reindex(columns=column_names01_05)

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        inner_joinOneAndFiveStyled = inner_joinOneAndFive.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Search Volume",
                "Salience URL #01",
                "Salience URL #05",
                "Ent. Count URL #01",
                "Ent. Count URL #05",
            ],
        ).background_gradient(
            cmap=cmRed,
            subset=[
                "Competition",
            ],
        )

        # Format as per format_dictionary
        inner_joinOneAndFiveStyled = inner_joinOneAndFiveStyled.format(
            format_dictionary
        )

        CSVButton5 = download_button(inner_joinOneAndFive, "Model5.csv", "Download CSV")
        st.table(inner_joinOneAndFiveStyled)

else:
    pass

# endregion urlFIVEnotONE ####################################################################################

# endregion [CSV_Button] IN OTHERS but not in ONE  ####################################################################################

# endregion [CSV_Button] ALL SUB LISTs   ####################################################################################

# endregion [CSV_Button] IN OTHERS BUT NOT ONE   ####################################################################################


# region [Master_File] ####################################################################################

st.markdown("")

st.markdown("### 🟡 **All results**")

dfColumnsList = df_merged.columns.tolist()

c10, c20 = st.columns(2)

col_one_list = df_merged["Entity Type"].tolist()
col_one_list = list(dict.fromkeys(col_one_list))

with c20:

    options = st.multiselect("Select entity types", col_one_list, col_one_list)

with c10:
    testone = st.multiselect(
        "Column selector",
        dfColumnsList,
        default=dfColumnsList,
        help="Check this box to enable xyz",
    )

dfFiltered2 = df_merged.loc[df_merged["Entity Type"].isin(options), testone]

CSVButtonMaster = download_button(
    dfFiltered2, "ModelMaster.csv", "Download Master file!"
)

# "dfFiltered2 LINKED TO DROPDOWNS!"
st.table(dfFiltered2)

# endregion [Master_File] ####################################################################################