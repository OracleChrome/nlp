# NLP Microservice
> Powerful NLP microservice that turns obtained webpage text into actionable items

## Invocation
This microservice is invoked by the NLP Backend API as `nlprouter.py {userId:string, webpageText:string}`, where `userId` is the primary id of the user as stored on the system and `webpageText`, the actual HTML text that is obtained from the client that is then cleansed, filtered and parsed.

When the microservice is invoked, an `NLPResultList` is returned, which is simply a JSON serialized list of objects that follow a certain schema. For more information on this schema, you can [visit the backend API documentation](https://github.com/OracleChrome/backend) for details.
