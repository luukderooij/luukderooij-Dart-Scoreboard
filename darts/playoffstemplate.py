
def playoffs_template(number_of_players=None, poule=1):
    if number_of_players is None:
        return None
    if poule == 1:  
        template = {
            # 2 players
            2: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 1, "player2": 2, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    }
                ]
            },

            # 3 players
            3: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 2, "player2": 3, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 2, "player1": 1, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 1}
                        ]
                    }
                ]
            },

            # 4 players
            4: {
                "rounds": [ 
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 1, "player2": 4, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 2, "player1": 2, "player2": 3, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 3, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 1, "p2_last_match_id": 2}
                        ]
                    }
                ]
            },

            # 5 players
            5: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 4, "player2": 5, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 2, "player1": 1, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 1},
                            {"match_id": 3, "player1": 2, "player2": 3, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                        ]
                    },
                    {
                        "round_id": 3,
                        "matches": [
                            {"match_id": 4, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 2, "p2_last_match_id": 3}
                        ]
                    }
                ]
            },

            # 6 players
            6: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 4, "player2": 5, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 2, "player1": 3, "player2": 6, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 3, "player1": 1, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 1},
                            {"match_id": 4, "player1": 2, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 2}
                        ]
                    },
                    {
                        "round_id": 3,
                        "matches": [
                            {"match_id": 5, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 3, "p2_last_match_id": 4}
                        ]
                    }
                ]
            },

            # 7 players
            7: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 2, "player2": 7, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 2, "player1": 3, "player2": 6, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 3, "player1": 4, "player2": 5, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 4, "player1": 1, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 1},
                            {"match_id": 5, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 2, "p2_last_match_id": 3}
                        ]
                    },
                    {
                        "round_id": 3,
                        "matches": [
                            {"match_id": 6, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 4, "p2_last_match_id": 5}
                        ]
                    }
                ]
            },

            # 8 players
            8: {
                "rounds": [
                    {
                        "round_id": 1,
                        "matches": [
                            {"match_id": 1, "player1": 1, "player2": 8, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 2, "player1": 2, "player2": 7, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 3, "player1": 3, "player2": 6, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None},
                            {"match_id": 4, "player1": 4, "player2": 5, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": None}
                        ]
                    },
                    {
                        "round_id": 2,
                        "matches": [
                            {"match_id": 5, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 1, "p2_last_match_id": 4},
                            {"match_id": 6, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 2, "p2_last_match_id": 3}
                        ]
                    },
                    {
                        "round_id": 3,
                        "matches": [
                            {"match_id": 7, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 5, "p2_last_match_id": 6}
                        ]
                    }
                ]
            }
        }

    if poule == 2:
        template = {
            # Is this one fair. Probably not. beacuase poule 1 is everytime the first one to get a bye

            #2 players
            2: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 15, "player1": 1, "player2": 1, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}
                            ]
                        }
                    ]
                },

            #3 players
            3: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 14, "player1": 1, "player2": 2, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None}
                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 15, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #4 players
            4: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 13, "player1": 1, "player2": 2, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 14, "player1": 1, "player2": 2, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None}
                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #5 players
            5: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                           ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 13, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": 1, "player2": 2, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None}
                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #6 players
            6: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": 3, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 13, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #7 players
            7: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 10, "player1": 1, "player2": 4, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": 3, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 13, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #8 players
            8: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": 4, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 10, "player1": 1, "player2": 4, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": 3, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #9 players
            9: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None}
                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": 4, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": 3, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #10 players
            10: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": 3, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #11 players
            11: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": 2, "player2": 3, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 12, "player1": 2, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #12 players
            12: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 5, "player1": 3, "player2": 6, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": 2, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 5},
                                {"match_id": 12, "player1": 2, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            #13 players
            13: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 3, "player1": 2, "player2": 7, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 5, "player1": 3, "player2": 6, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 3, "p2_last_match_id": 5},
                                {"match_id": 12, "player1": 2, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },
       
            #14 players
            14: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 3, "player1": 2, "player2": 7, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 4, "player1": 2, "player2": 7, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 5, "player1": 3, "player2": 6, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": 1, "player2": None, "p1_poule_id": 2, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 3, "p2_last_match_id": 5},
                                {"match_id": 12, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 4, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            # 15 players
            15: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 2, "player1": 1, "player2": 8, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 3, "player1": 2, "player2": 7, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 4, "player1": 2, "player2": 7, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 5, "player1": 3, "player2": 6, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": 1, "player2": None, "p1_poule_id": 1, "p2_poule_id": None, "p1_last_match_id": None, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 2, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 3, "p2_last_match_id": 5},
                                {"match_id": 12, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 4, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                },

            # 16 players
            16: {
                    "rounds": [
                        {
                            "round_id": 1,
                            "matches": [
                                {"match_id": 1, "player1": 1, "player2": 8, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 2, "player1": 1, "player2": 8, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 3, "player1": 2, "player2": 7, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 4, "player1": 2, "player2": 7, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 5, "player1": 3, "player2": 6, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 6, "player1": 3, "player2": 6, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 7, "player1": 4, "player2": 5, "p1_poule_id": 2, "p2_poule_id": 1, "p1_last_match_id": None, "p2_last_match_id": None},
                                {"match_id": 8, "player1": 4, "player2": 5, "p1_poule_id": 1, "p2_poule_id": 2, "p1_last_match_id": None, "p2_last_match_id": None}

                            ]
                        },
                        {
                            "round_id": 2,
                            "matches": [
                                {"match_id": 9, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 1, "p2_last_match_id": 7},
                                {"match_id": 10, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 2, "p2_last_match_id": 8},
                                {"match_id": 11, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 3, "p2_last_match_id": 5},
                                {"match_id": 12, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 4, "p2_last_match_id": 6}

                            ]
                        },
                        {
                            "round_id": 3,
                            "matches": [
                                {"match_id": 13, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 9, "p2_last_match_id": 11},
                                {"match_id": 14, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 10, "p2_last_match_id": 12}
                            ]
                        },
                        {
                            "round_id": 4,
                            "matches": [
                                {"match_id": 15, "player1": None, "player2": None, "p1_poule_id": None, "p2_poule_id": None, "p1_last_match_id": 13, "p2_last_match_id": 14}
                            ]
                        }
                    ]
                }
            }


    return template.get(number_of_players, None)




