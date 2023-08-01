# *Reflections of Life*

GoIT Python Web Group 3 Project

## *Desription*

Reflection of Life is web application that helps people to share their photos with others.

#### _With Reflections of Life you can:_
- show your beautiful photos to all world;
- add tags and description to photo;
- comment photos;
- rate photos;
- transform photos;
- search photo by it's keyword;
- create your profile with personal info.

## **Routes:**

| Route | Parameters | Output |
|-------| ---------- | ------ |
| GET / | skip(query), limit(query) | List of all photos |

### Authentification

| Route                                 | Parameters                | Output                                 |
|---------------------------------------|---------------------------|----------------------------------------|
| GET /api/auth/signup                  | username, email, password | Create new account.                    |
| GET /api/auth/login                   | username, password        | Login.                                 |
| GET /api/auth/logout                  | -                         | Logout.                                |
| GET /api/auth/refresh_token           | -                         | Refresh Token.                         |
| GET /api/auth/confirmed_email/{token} | token                     | Confirm email.                         |
| GET /api/auth/request_email           | email | Send new confirmation letter on email. |

### User Profile
| Route | Parameters | Output                        |
| ----- | ---------- |-------------------------------|
|GET /api/users/me | - | Show profile info.            |
| PUT /api/users/me | username, about, birthday, country, phone | Add personal info to profile. | 
| GET /api/users/{user_id} | user_id(query) | Show profile of user.         |

### Admin Profile

| Route | Parameters | Output                        |
| ----- | ---------- |-------------------------------|
| PUT /api/admin/users/{user_id}/status | user_id(query), status | Change status of user (ban) |
| PUT /api/admin/users/{user_id}/role | user_id(query), role | Change user's role |

### Operations with photos

| Route | Parameters | Output                        |
| ----- | ---------- |-------------------------------|
| GET /api/photos/ | - | Show current user's photos.   |
| POST /api/photos/upload | description, src-url, tags | Add new photo.                |
| GET /api/photos/{photo_id} | photo_id | Show photo ifo with comments. |
| DELETE /api/photos/{photo_id} | photo_id | Delete photo. |
| PUT /api/photos/{photo_id} | photo_id | Change photo description. |
| GET /api/photos/search_keyword | search_by, filter_by | Search photo by keyword. |
| GET /api/photos/{photo_id}/resize | photo_id(query), width, height | Change photo size. |
| GET /api/photos/{photo_id}/crop | photo_id(query), x, y, width, height | Crop photo. |
| GET /api/photos/{photo_id}/rotate | photo_id(query), angle | Rotate photo. |
| GET /api/photos/transform_and_create_link | photo_id, width, height | Transform photo and create link. |

### Comments

| Route | Parameters | Output                        |
| ----- | ---------- |-------------------------------|
| POST /api/photos/{photo_id} | photo_id(query), comment | Add comment. |
| PATCH /api/photos/{photo_id}/{comment_id} | photo_id(query), comment_id(query), comment | Change comment. |
| DELETE /api/photos/{photo_id}/{comment_id} | photo_id(query), comment_id(query) | Delete comment. |

### Rating 

| Route | Parameters | Output                        |
| ----- | ---------- |-------------------------------|
| GET /api/rating |limit(query), offset(query) | Show photos' rating|
| POST /api/rating | photo_id, rate | Rate photo. |
| GET /api/rating/{photo_id} | photo_id(query) | Show photo's average rating. |
| DELETE /api/rating/{rating_id} | rating_id(query) | Delete rate. |

---

## About our team
### SUPERTEAM
- Team Leader: Maryna Zipova
- Scrum Master: Tetiana Karaschenko
- Python Developers: Dzvenyslava Vovk, Ira Dachuk


