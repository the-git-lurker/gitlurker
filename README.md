# GitLurker

### Overview:
Simple web app built with Django to summarize data from a range of GitHub repositories.

Upon loading the page you will see information related to the the projects and their latest releases. With data sorted newest to oldest and a range of category tabs.

Don't be alarmed if some pages take a little time to load. If the data are older than 3 hours the application will fetch new data from the GitHub API. Otherwise, if the data are more recent it will be pulled from the back-end database.

**Website:** [www.gitlurker.info](https://www.gitlurker.info/)

With the `All` tab selected we have the following main categories:
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

Follow: [npub1cy80mfgpy2h0zs5kzze978qqnc8mlrlmeu70ldsvgkywk3vwlz5qlv3sfd](https://primal.net/p/npub1cy80mfgpy2h0zs5kzze978qqnc8mlrlmeu70ldsvgkywk3vwlz5qlv3sfd)

The website now sends Nostr events for new releases automatically (after some spam teething issues thanks my inexpereince building Nostr integrated stuff). 

By following the project you'll get updates on the GitHub projects we list directly in your feed. 

For the second stage of this process I also hope to add some information to the release pages so that we can see any replies to these automated posts. Just as a nice way to show what people are saying about the new release.

Watch this space, 2 weeks, soon...<sup>TM</sup>

---

### Feedback
If you would like to request any features or the addition of any specific projects please feel free to drop an email to: gitlurker@proton.me

Support and Feedback are always welcome.

