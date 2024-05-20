import customtkinter as ctk


"""
        USER TEMPLATE:
            {
                "fullName": "",
                "roles": [],
                "profilePic": "",
                "photos": [],
                "videos": [],
                "biography": "",
                "movies": "",
                "moviesSeparatedByRoles": {
                                            "actress": [
                                                        {each movie has been populated here}
                                                        ]
                                            },
                "height": 0,
                "birthDate": "",
                "birthPlace": "",
                "comments": [
                        {each comment has been populated here}
                ]
            }
"""


class CastPage(ctk.CTkScrollableFrame):
    def __init__(self, master, user, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        