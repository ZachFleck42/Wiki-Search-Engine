from ahocorapy.keywordtree import KeywordTree
from src.database_utils import fetchAllData
from src.search_algorithms.boyer_moore import BMsearch
from src.search_algorithms.knuth_morris_pratt import KMPsearch
from src.search_algorithms.robin_karp import RKsearch


def runSearch(tableName, userInput, searchMethod=1):
    '''
    Parent function for running a search for userInput in tableName.
    Also allows for the selection of one of five different search methods 
        (default is python str.count() method)
    Returns a sorted list of results, each taking the form:
        ("pageTitle", No. of occurrences of userInput on page)
    '''
    # Read website data into the program from database
    rows = fetchAllData(tableName)
    needle = userInput.lower()
    
    # Store the search results in a dictionary
    searchResults = {}
    for row in rows:
        needleOccurrences = 0
        haystack = row[3]
        if searchMethod == "COUNT":       # Search method is Python str.count() method
            needleOccurrences = (haystack.count(needle))
        elif searchMethod == "BM":     # Search method is Boyer-Moore algorithm
            needleOccurrences = len(BMsearch(needle, haystack))
        elif searchMethod == "KMP":     # Search method is Knuth-Morris-Pratt algorithm
            needleOccurrences = len(KMPsearch(needle, haystack))
        elif searchMethod == "RK":     # Search method is Robin-Karp algorithm
            needleOccurrences = len(RKsearch(needle, haystack))
        elif searchMethod == "AC":     # Search method is Aho-Corasick algorithm
            kwtree = KeywordTree(case_insensitive=True)
            kwtree.add(needle)
            kwtree.finalize()
            if resultsFound := kwtree.search_all(haystack):
                needleOccurrences = sum(1 for result in resultsFound)
        
        # Append results to the dictionary
        pageTitle = row[1]
        searchResults[pageTitle] = needleOccurrences
            
    # Sort and return the list of results
    searchResultsSorted = sorted(searchResults.items(), key=lambda x: x[1], reverse=True)
    return(searchResultsSorted)