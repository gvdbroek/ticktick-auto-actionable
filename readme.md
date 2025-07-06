# Ticktick Auto-Actionable

This script checks your todo lists in TickTick and verifies if any of its tasks (or subtasks) contain a tag called 'next'.
If this does not exist, a new high-priority task will be created.

## What is Actionability?
I'd define actionable as: _it has a chosen next step to be fulfilled_
Especially in big task lists, where you have 50 todo's, you might want to pick out 1 item that is the next thing you could/should do.
Another part of actionability is setting **deadlines**

There's 3 kinds of actionability: 'next', 'waiting', 'choose'. They can be used individually, or a combination of any 2 options.

**next:** Marking a task as your next best action make it so you always know exactly what you want to do next.

**waiting:** Means that you're being blocked, or are waiting for something before this task can proceed.

**choose:** Maybe a bit contentious, but it indicates that an important decision has to be made. Before taking any other action

### Combined types
**next & waiting:** You are literally blocked and cannot proceed until the 'wait' has lifted. No other action can be taken in your project. Tasks like this should normally also have a 'deadline' associated with them. When the deadline expires, SOME action has to be taken.
It can mean, extend the deadline, OR find another thing. Depending on your project needs.

**next & choose:** You MUST make a choice before proceeding with your task, but a choice has to be made.

**waiting & choose:** The odd-one in the bunch, to me this means that we're waiting for some information or someone's feedback before we can make an important decision.

**next, waiting & choose:** probably shouldn't happen anyway.


## Why?
I often lose track of projects when they are no longer 'actionable', or when I have no 'next thing to do' for them.
So the idea was, make it so that every list HAS to be actionable. So to expand on that idea, any list that has no actionable item is considered stale.
So when the script detects this, a new task will be created in that list that urges you to choose a 'next' item.

## Deployment
This is the first time I've made a serverless thing for myself, the intention is there to make this into a docker container but I need to figure out what architecture I really want to evolve to. A cloud run function was an easy way for me to get this up and running

### Getting a ticktick api key
Unfortunatly, the ticktick api is not the best documented thing out there. And the python-ticktick module is a bit dated I believe.  
For the time being, provide your own api key. Luckily the key you get from ticktick is valid for a year (refresh must happen at 31 december I think). This is another thing I want to simplify a bit at some point. But for the time being I'm just using a postman call and copy pasting the api key into the gcloud secret variable called api-key. 
#### postman
Load the ticktick.postman_collection.json into postman, set up 3 env vars: `base_url`, `client_id` & `client_secret` , click the collection's folder, and request a new api-key, go through the flow and you should see the Access-Token field be filled with your api key.


## Usage
1. Get a ticktick api key for your account.
2. Deploy the script and set a cron-job  
*If you're using gcloud, you can run the 'deploy.sh' script if you want*
3. Done
