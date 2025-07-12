job_search_query = """
    query GetJobData {{
        jobSearch(
        {what}
        {location}
        limit: 100
        {cursor}
        sort: RELEVANCE
        {filters}
        ) {{
        pageInfo {{
            nextCursor
        }}
        results {{
            trackingKey
            job {{
            source {{
                name
            }}
            key
            title
            datePublished
            dateOnIndeed
            description {{
                html
            }}
            location {{
                countryName
                countryCode
                admin1Code
                city
                postalCode
                streetAddress
                formatted {{
                short
                long
                }}
            }}
            compensation {{
                estimated {{
                currencyCode
                baseSalary {{
                    unitOfWork
                    range {{
                    ... on Range {{
                        min
                        max
                    }}
                    }}
                }}
                }}
                baseSalary {{
                unitOfWork
                range {{
                    ... on Range {{
                    min
                    max
                    }}
                }}
                }}
                currencyCode
            }}
            attributes {{
                key
                label
            }}
            employer {{
                relativeCompanyPageUrl
                name
                dossier {{
                    employerDetails {{
                    addresses
                    industry
                    employeesLocalizedLabel
                    revenueLocalizedLabel
                    briefDescription
                    ceoName
                    ceoPhotoUrl
                    }}
                    images {{
                        headerImageUrl
                        squareLogoUrl
                    }}
                    links {{
                    corporateWebsite
                }}
                }}
            }}
            recruit {{
                viewJobUrl
                detailedSalary
                workSchedule
            }}
            }}
        }}
        }}
    }}
    """

api_headers = {
    "Host": "apis.indeed.com",
    "content-type": "application/json",
    "indeed-api-key": "161092c2017b5bbab13edb12461a62d5a833871e7cad6d9d475304573de67ac8",
    "accept": "application/json",
    "indeed-locale": "en-US",
    "accept-language": "en-US,en;q=0.9",
    "indeed-app-info": "appv=205.0; appid=com.indeed.jobsearch; osv=17.4.1; os=ios; dtype=phone",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
}
