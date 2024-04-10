# GitLurker

### Overview:
Simple web app built with Django to summarize data from a range of GitHub repositories.

Upon loading the page you will see information related to the the projects and their latest releases. With data sorted newest to oldest and a range of category tabs.

Don't be alarmed if some pages take a little time to load. If the data are older than 3 hours the application will fetch new data from the GitHub API. Otherwise, if the data are more recent it will be pulled from the back-end database.

With the `All` tab we have the following main category symbols for:
- **Bitcoin**
- **Lightning**
- **e-Cash**
- **Nostr**
- **Other**

When a user navigates to one of these separate tabs they will see the following sub-categorisation:
- **Client** / **Relay**: mostly relevant for Nostr projects
- **Development**: tools/repositories that are used during development or as a source library for other projects
- **Exchange**
- **Interface**: including projects which provide extended function to or interface with the underlying protocol or plug-in to another project
- **Node**: includes 'node-in-a-box' solutions, predominantly for lightning
- **Wallet**: projects that provide users with means of maintaining balances, funds and making payments, for e-Cash this includes mints
- **Server**: much like nodes but home server projects
- **Payments**: includes payment systems including collaborative payjoin
- **Protocol**: protocols and related implementations
- **Signer**: projects specifically focused on signing devices
- **Other**

---
### Nostr Integration:
As well as being able to visit this site to get information about specific projects there is a plan to also produce Nostr events for new releases and share this information automatically. This will allow you to follow the project on NOSTR and see these updates appear directly in your feed. 

This function is currently in testing and will be rolled out in the coming weeks.

---

### Feedback
If you would like to request any features or the addition of any specific projects please feel free to drop an email to: gitlurker@proton.me

Support and Feedback are always welcome.

