MESSAGE_PATH = "message.txt"
PROGRAM_PATH = "src\query_receive.py"

QUERY_RECEIVE = "src\query_receive.py"

# deepseek
API_KEY = ""
BASE_URL = "https://api.deepseek.com"
GLOBAL_MODEL = "deepseek-chat"

# qwen
# API_KEY="",
# BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1",
# GLOBAL_MODEL = "qwen-plus"

# gpt-4o
# API_KEY="",
# BASE_URL="https://api.chatanywhere.tech",
# GLOBAL_MODEL = "gpt-4o"

MESSAGE_PLANNER = [
    """Your tools are as follows:
RealTimeAmazonData	"{
""country"": {
""type"": ""String"",
""required"": false,
""description"": ""Sets the Amazon domain, marketplace country, language and currency. Default: us. Allowed values: us, TR.""
},
""offset"": {
""type"": ""Number"",
""required"": false,
""description"": ""Number of results to skip / index to start from (for pagination).""
},
""categories"": {
""type"": ""String"",
""required"": false,
""description"": ""Return deals with products in specific categories / departments. Multiple categories can be specified as a comma (,) separated list. Numeric category id's can be found in the URL after selecting a specific category on https://www.amazon.com/deals.""
},
""min_product_star_rating"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Return deals with products star rating greater than a specific value. Default: ALL. Allowed values: ALL, 1, 2, 3, 4.""
},
""price_range"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Return deals with price within a specific price range. 1 is lowest price range shown on Amazon (e.g. Under $25) while 5 is the highest price range (e.g. $200 & Above). Default: ALL. Allowed values: ALL, 1, 2, 3, 4, 5.""
},
""discount_range"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Return deals with discount within a specific discount range. 1 is lowest discount range shown on Amazon (e.g. 10 % off or more) while 5 is the highest discount range (e.g. 70 % off or more). Default: ALL. Allowed values: ALL, 1, 2, 3, 4, 5.""
},
""brands"": {
""type"": ""String"",
""required"": false,
""description"": ""Return deals with products by specific brands. Multiple brands can be specified separated by comma (,). In addition, brand names can be found under the Brand filter on the filter/refinements panel on https://www.amazon.com/deals (when applicable).""
},
""prime_early_access"": {
""type"": ""Boolean"",
""required"": false,
""description"": ""Only return prime early access deals.""
},
""prime_exclusive"": {
""type"": ""Boolean"",
""required"": false,
""description"": ""Only return prime exclusive deals.""
},
""fields"": {
""type"": ""String"",
""required"": false,
""description"": ""A comma separated list of deal fields to include in the response (field projection). By default all fields are returned.""
}
}"
RealTimeProductSearch	"{
""q"": {
""type"": ""str"",
""required"": true,
""description"": ""Search query /keyword. Must be provided.""
},
""language"": {
""type"": ""str"",
""required"": false,
""description"": ""The language of the results. Default: en.""
},
""page"": {
""type"": ""Number"",
""required"": false,
""description"": ""Results page to return (each page contains up to 100 product results). Default: 1. Allowed values: 1 - 100.""
},
""limit"": {
""type"": ""Number"",
""required"": false,
""description"": ""Maximum number of products to return. Default: 30. Allowed values: 1 - 100.""
},
""sort_by"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Sort product offers by best match, top rated, lowest or highest price. Default: BEST_MATCH. Allowed values: BEST_MATCH, LOWEST_PRICE, HIGHEST_PRICE.""
},
""min_price"": {
""type"": ""Number"",
""required"": false,
""description"": ""Only return product offers with price greater than a certain value.""
},
""max_price"": {
""type"": ""Number"",
""required"": false,
""description"": ""Only return product offers with price lower than a certain value.""
},
""product_condition"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Only return products with a specific condition. Default: ANY. Allowed values: ANY, NEW, USED, REFURBISHED.""
},
""stores"": {
""type"": ""String"",
""required"": false,
""description"": ""Only return product offers from specific stores. Accepts a single or a comma delimited list of store names (e.g. best buy, walmart, amazon).""
},
""free_returns"": {
""type"": ""Boolean"",
""required"": false,
""description"": ""Only return product offers that offer free returns. Default: false.""
},
""free_shipping"": {
""type"": ""Boolean"",
""required"": false,
""description"": ""Only return product offers that offer free shipping/delivery. Default: false.""
},
""on_sale"": {
""type"": ""Boolean"",
""required"": false,
""description"": ""Only return product offers that are currently on sale. Default: false.""
}
}"
ShopeeEcommerceData	"{
""site"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Optional values: my, th, vn, ph, sg, id, tw, br.""
},
""keyword"": {
""type"": ""String"",
""required"": false,
""description"": ""Keyword for search.""
},
""by"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Unspecified.""
},
""order"": {
""type"": ""Enum"",
""required"": false,
""description"": ""Unspecified.""
},
""page"": {
""type"": ""Number"",
""required"": false,
""description"": ""Page number.""
},
""pageSize"": {
""type"": ""Number"",
""required"": false,
""description"": ""Number of items per page.""
},
""cat_ids"": {
""type"": ""String"",
""required"": false,
""description"": ""Category IDs, you can set single category or separate multiple ids with commas. If you don't need to search keywords, just set 'keyword' to empty string.""
},
""price_start"": {
""type"": ""String"",
""required"": false,
""description"": ""Minimum value of price range filter.""
},
""price_end"": {
""type"": ""String"",
""required"": false,
""description"": ""Maximum value of price range filter.""
}
}"
The task is:
"""
]
MESSAGE_RESULT = [
    """
Your tools are as follows:
Your tools response are as follows:
"RealTimeAmazonData:
{
""type"": ""object"",
""properties"": {
""status"": {
    ""type"": ""string""
},
""request_id"": {
    ""type"": ""string""
},
""data"": {
    ""type"": ""array"",
    ""items"": {
    ""type"": ""object"",
    ""properties"": {
        ""id"": {
        ""type"": ""string""
        },
        ""name"": {
        ""type"": ""string""
        }
    }
    }
}
}
}"
"RealTimeProductSearch:
{
""type"": ""object"",
""properties"": {
""status"": {
    ""type"": ""string""
},
""request_id"": {
    ""type"": ""string""
},
""data"": {
    ""type"": ""object"",
    ""properties"": {
    ""products"": {
        ""type"": ""array"",
        ""items"": {
        ""type"": ""object""
        }
    },
    ""sponsored_products"": {
        ""type"": ""array"",
        ""items"": {
        ""type"": ""object"",
        ""properties"": {
            ""offer_id"": {
            ""type"": ""string""
            },
            ""offer_page_url"": {
            ""type"": ""string""
            },
            ""title"": {
            ""type"": ""string""
            },
            ""photo"": {
            ""type"": ""string""
            },
            ""merchant_id"": {
            ""type"": ""string""
            },
            ""store_name"": {
            ""type"": ""string""
            }
        }
        }
    }
    }
}
}
}"
"ShopeeEcommerceData:
{
""type"": ""object"",
""properties"": {
""code"": {
    ""type"": ""integer""
},
""msg"": {
    ""type"": ""string""
},
""data"": {
    ""type"": ""object"",
    ""properties"": {
    ""item_id"": {
        ""type"": ""string""
    },
    ""shop_id"": {
        ""type"": ""string""
    },
    ""site"": {
        ""type"": ""string""
    },
    ""page"": {
        ""type"": ""integer""
    },
    ""page_size"": {
        ""type"": ""integer""
    },
    ""rate_filter"": {
        ""type"": ""string""
    },
    ""rate_star"": {
        ""type"": ""string""
    },
    ""total_count"": {
        ""type"": ""integer""
    },
    ""has_next_page"": {
        ""type"": ""boolean""
    },
    ""ratings"": {
        ""type"": ""array"",
        ""items"": {
        ""type"": ""object"",
        ""properties"": {
            ""anonymous"": {
            ""type"": ""boolean""
            },
            ""author_username"": {
            ""type"": ""string""
            },
            ""author_userid"": {
            ""type"": ""string""
            },
            ""comment"": {
            ""type"": ""string""
            },
            ""ctime"": {
            ""type"": ""integer""
            },
            ""is_hidden"": {
            ""type"": ""boolean""
            },
            ""is_repeated_purchase"": {
            ""type"": ""boolean""
            },
            ""like_count"": {
            ""type"": [""integer"", ""null""]
            },
            ""order_id"": {
            ""type"": ""string""
            },
            ""rating_star"": {
            ""type"": ""integer""
            },
            ""rating_star_detail"": {
            ""type"": ""object"",
            ""properties"": {
                ""product_quality"": {
                ""type"": ""integer""
                }
            }
            },
            ""rating_imgs"": {
            ""type"": ""array"",
            ""items"": {
                ""type"": ""string""
            }
            },
            ""rating_videos"": {
            ""type"": ""array"",
            ""items"": {
                ""type"": ""string""
            }
            },
            ""status"": {
            ""type"": ""integer""
            }
        }
        }
    }
    }
}
}
}"
"""
]
