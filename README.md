# Robodev AI

Robodev AI is an AI software engineering agent that can generate full backend applications from an app description. 

It was built back when `text-davinci-003` was the state-of-the-art LLM and we didn't have the convenience of structured 
outputs, so naturally, it is a bit outdated.

The basic premise was to break the process of building a backend into simpler, generalizable steps, which could be 
completed by an LLM, for example, generating the table names for the database, the data schema, the API routes, etc. 
Then once we had the high level design, implement specific logic for individual functions.

The end goal was to use the LLM to come up with a `Buildfile`, which could then be directly compiled into code, something like:
```
{
  "project_name": "my_app",
  "db_params": [],
  "relations": [],
  "controllers": [],
  "routes": [],
  "middlewares": [],
  "mailers": [],
  "auth": {},
  "auth_object": null,
  "email": "",
  "config": {
    "email": "",
    "server_port": 8080,
    "db_url": ""
  }
}
```

The Buildfile was designed to be generic and language agnostic, so that if the user wanted to generate apps in Python or 
JavaScript, or Rails, they'd be able to do so just as easily. 

The LLM, then wouldn't have to generate the entire codebase from scratch, but instead auto-complete prompts like:
```
You are an AI support bot in charge of helping a user design a database architecture given an app description.
Your job is to identify which database tables would be required to build out a proper database for this app.
All tables should be PascalCase and singular.
If a table is meant to be a joint table for handling many-to-many relationships, add an * at the end

Human:
I want to build a blog app where users can make posts and comment on posts as well as join groups and like posts
to talk about specific issues. Users can also follow other users.
What database tables would be required?

AI:
User,Post,Comment,Group,Like*,Follow*

Human:
I want to build a simple AirBnB style app where users can sign up as hosts to rent out their houses and other users can
sign up as guests to stay at others' houses.
What database tables would be required?

AI:
User,Host,Listing,Booking,Review,Amenities,Location

Human:
Ecommerce site like Amazon
User,Product,Order,OrderItem*,Category,ProductCategory*,Review,Cart

Human:
$$APP_DESCRIPTION$$
What database tables would be required?

AI:

```

Since Davinci was not too good at generating bug-free, up-to-date Node/Express code, we also had to incorporate a few 
hacks to minimize the number of bugs in the more specific app logic.   
Particularly, this involved having the LLM write a custom pseudocode syntax as opposed to javascript code directly. 
Something like:
```
QUERY User; { _id: req.params.follower_id }; false -> follower
    IF follower 
        QUERY User; { _id: req.params.followed_id }; false -> followed
        IF followed 
            UPDATE User; { _id: follower._id }; { $push: { following: followed._id } }
                =>
                <=
                =x
                ERROR 500; "error following"
                x=
            UPDATE User; { _id: followed._id }; { $push: { followers: follower._id } }
                =>
                <=
                =x
                ERROR 500; "error following"
                x=
            RETURN 200; "followed successfully"
        ELSE
            ERROR 404; "followed user not found"
    ELSE 
        ERROR 404; "follower user not found"
        PASS
```
