from JsonDemo import DateSearch, JsonRequestor

def main():
    url_head = 'https://www1.hkexnews.hk/search/titleSearchServlet.do?sortDir=0' \
               '&sortByOptions=DateTime&category=0&market=SEHK&stockId=-1&documentType=-1&fromDate='
    # from_date = '20240612'
    # to_date = '20240712'

    # search can only be completed with time span no more than one month.
    date_searcher = DateSearch()
    from_date, to_date = date_searcher.getSearchWindow(1)
    print(from_date, to_date)

    url_tail = '&title=&searchType=0&t1code=-2&t2Gcode=-2&t2code=-2&rowRange=10&lang=E'
    url = url_head + from_date + '&toDate=' + to_date + url_tail

    # =============================
    # please change the download dir
    # windows output_dir
    # output_dir = 'D:/Dev/downloads'

    # mac output_dir
    output_dir = '/Users/apple/Dev/downloads'
    esg_pattern = re.compile(r'\b(ESG|environment|environmental)\b', re.IGNORECASE)
    download_files(url, output_dir, esg_pattern)

if __name__ == "__main__":
    main()