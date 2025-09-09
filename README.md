#  Multi-Language Intent Finder

This tool helps you locate `@intent:` comments across your codebase.  

Comments don’t have to be just plain notes about what your code does. They can serve a bigger purpose: provide context, convey intent, link to ticket numbers, include tags, or even add a touch of humor. With `@intent:`, your comments become **structured, meaningful metadata** that both humans and AI can understand.

---

## ✍️ What is `@intent:`?

Think of `@intent:` like **a sticky note for your code**.  

- It tells people (and AI) **what this function or code block is supposed to do**.  
- You can also add **ticket numbers** or **tags** to give extra info.  

Examples
```
#!/bin/bash

# @intent: backup database | ticket: DB-789 | cronjob
# Backing up DB so intense, even the server is sweating 😅
mysqldump mydb > backup.sql
```

```python
# @intent: camping snack prep | ticket: FUN-002 | joke
# Preparing s'mores for our Taal glamping trip… INTENTS all around 🍫🔥
prepare_smores() {
    echo "Chocolate + marshmallows + graham crackers = intense snack!"
}
```
