## local-viral-dashboard
This was a viral DC metro real-time application and covid dashboard created as part of a Axio's 3 days hackathon.

Our application is hosted by [Heroku](https://www.heroku.com/). 

**note** -> Due to Heroku's latest policy changes as a paid service for using dynos features, it's no longer an open source platform.

Tech stack used: 
- Flask - Python microservice web framework
- HTML/CSS - frontend development and design
- Heroku - (no longer) open source cloud hosting service
- CI/CD deployment - Heroku's dynos - a lightweight Linux containers that runs our application and processes. When it gets deployed, the dynos are executed to run our web processes. And any changes made through Github will automatically deployed through the dynos in Heroku.

- Live website -> https://axios-dc-live.herokuapp.com/ (deprecated - see note)
- Linked real-time covid dashboard -> https://axios-live-dc-covid.herokuapp.com/ (deprecated - see note)
