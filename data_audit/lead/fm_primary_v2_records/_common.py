"""Shared helpers + record schema for the PRIMARY FM candidate survey v2.

Every quote is Q(text, file) where file is the stem of a saved copy
fm_sources/primary/<file>.txt; the builder verifies it (whitespace-normalised substring) and adds
source_url + saved_copy.  Record keys (all entries):

  name, aliases, paper{title,year,venue,arxiv,quotes}
  version{value,basis,quotes}
  weights_location{url,exists,access,verification,quotes}
  licence{code,weights,url,code_and_weights_differ,quotes}
  domain{value,quotes}
  pretraining_data_quote{summary,datasets,quotes}
  appendix300_check{answer,quote_or_statement,quote_or_statement_is_verbatim,cannot_exclude_note,quotes}
  input{frame_size,frame_rate_or_sampling,clip_length_frames,notes,quotes}
  embedding_dim{value,basis,quotes}
  params{value,quotes}
  flops_per_input_if_documented{value(None if undocumented),statement,quotes}
  eligibility{open_weights,licence_research_use,domain_primary,documented_pretraining_data: {status,basis}; eligible}
  changes_vs_previous (old entries only), legacy fields of the first partial pass (old entries only)
"""

NOT_MENTIONED = "the documented data list does not mention DS203/Appendix300"
CENTRES = ("University Hospital Carl Gustav Carus Dresden, Asklepios-ASB Radeberg, St. Elisabethen-Klinikum "
           "Ravensburg, St. Joseph-Stift Dresden, Diakonissenkrankenhaus Dresden, Dresden-Friedrichstadt")


def Q(quote, file):
    return {"quote": quote, "file": file}


def C(status, basis):
    assert status in ("PASS", "FAIL", "UNKNOWN"), status
    return {"status": status, "basis": basis}


def elig(open_weights, licence, domain, data, notes=""):
    sts = [x["status"] for x in (open_weights, licence, domain, data)]
    overall = "FAIL" if "FAIL" in sts else ("UNKNOWN" if "UNKNOWN" in sts else "PASS")
    return {"open_weights": open_weights, "licence_research_use": licence, "domain_primary": domain,
            "documented_pretraining_data": data, "eligible": overall, "notes": notes}


def A300(answer, quote_or_statement, verbatim, cannot_exclude_note, quotes=()):
    assert answer in ("YES", "NO", "UNKNOWN")
    return {"answer": answer, "quote_or_statement": quote_or_statement,
            "quote_or_statement_is_verbatim": verbatim, "cannot_exclude_note": cannot_exclude_note,
            "centres_searched_for": CENTRES, "quotes": list(quotes)}


def NOFLOPS(searched):
    return {"value": None, "statement": f"not documented in the saved sources (searched: {searched})", "quotes": []}
