# API仕様書
---
## https://api/
### 共通
```Content-Type: application/json```

---
### GET users/
登録されているUserの一覧を返す
#### クエリパラメータ
|名前|型|必須|値の説明|
|:-|-|-|:-|
|limit|数値|　|何件取得するかの指定（指定なしは100件）|
|offset|数値||何件目から切り出すかの指定|
#### 結果
```
[
    "count": 4,
    "next": null,
    "previous": null
    {
        "id": 1,
        "name": "",
        "icon": null,
        "profile": "",
        "my_link": [],
        "my_ladders": []
    },
    {
        "id": 2,
        "name": "shun5",
        "icon": null,
        "profile": "",
        "my_link": [],
        "my_ladders": [
            {
                "id": 2,
                "title": "python",
                "user": "shun5",
                "created_at": "2018-07-15T00:52:14.511474Z"
            },
            {
                "id": 3,
                "title": "pyython",
                "user": "shun5",
                "created_at": "2018-07-15T00:52:36.951966Z"
            },
            {
                "id": 4,
                "title": "pyythonn",
                "user": "shun5",
                "created_at": "2018-07-15T00:58:52.003245Z"
            },
            {
                "id": 5,
                "title": "pyythonnn",
                "user": "shun5",
                "created_at": "2018-07-15T11:35:38.395695Z"
            },
            {
                "id": 6,
                "title": "pythoon",
                "user": "shun5",
                "created_at": "2018-07-15T11:37:40.463821Z"
            },
            {
                "id": 1,
                "title": "pypython",
                "user": "shun5",
                "created_at": "2018-07-14T15:59:51.940872Z"
            },
            {
                "id": 8,
                "title": "test",
                "user": "shun5",
                "created_at": "2018-07-18T05:50:46.496288Z"
            },
            {
                "id": 9,
                "title": "aaa",
                "user": "shun5",
                "created_at": "2018-07-19T12:17:52.984974Z"
            }
        ]
    },
    {
        "id": 3,
        "name": "funashi",
        "icon": null,
        "profile": "",
        "my_link": [],
        "my_ladders": [
            {
                "id": 7,
                "title": "python入門",
                "user": "funashi",
                "created_at": "2018-07-15T12:09:43.787345Z"
            }
        ]
    },
    {
        "id": 4,
        "name": "ryo",
        "icon": null,
        "profile": "",
        "my_link": [],
        "my_ladders": []
    },
    {
        "id": 28,
        "name": "test君",
        "icon": null,
        "profile": "",
        "my_link": [],
        "my_ladders": []
    }
]
```
### POST users/
ユーザーの登録
#### 入力
|JSON key|型|必須|値の説明|
|:-------|-|-|:----|
|name|文字列|○|ユーザーの名前|
|email|メールアドレス|○|メールアドレス|
|icon|ファイル|　|アイコンの画像ファイル|
|profile|文字列||ユーザーの自己紹介文|
|password|文字列|○|パスワード|

#### 結果
```

{
    "id": 30,
    "name": "test君",
    "icon": null,
    "profile": "",
    "my_link": [],
    "my_ladders": []
}
```
### GET users/:id
指定されたidのユーザーを返します
#### 結果
```
{
    "id": 2,
    "name": "shun5",
    "icon": null,
    "profile": "",
    "my_link": [],
    "my_ladders": [
        {
            "id": 2,
            "title": "python",
            "user": "shun5",
            "created_at": "2018-07-15T00:52:14.511474Z"
        },
        {
            "id": 3,
            "title": "pyython",
            "user": "shun5",
            "created_at": "2018-07-15T00:52:36.951966Z"
        },
        {
            "id": 4,
            "title": "pyythonn",
            "user": "shun5",
            "created_at": "2018-07-15T00:58:52.003245Z"
        },
        {
            "id": 5,
            "title": "pyythonnn",
            "user": "shun5",
            "created_at": "2018-07-15T11:35:38.395695Z"
        },
        {
            "id": 6,
            "title": "pythoon",
            "user": "shun5",
            "created_at": "2018-07-15T11:37:40.463821Z"
        },
        {
            "id": 1,
            "title": "pypython",
            "user": "shun5",
            "created_at": "2018-07-14T15:59:51.940872Z"
        },
        {
            "id": 8,
            "title": "test",
            "user": "shun5",
            "created_at": "2018-07-18T05:50:46.496288Z"
        },
        {
            "id": 9,
            "title": "aaa",
            "user": "shun5",
            "created_at": "2018-07-19T12:17:52.984974Z"
        }
    ]
}
```

### GET users/:id/learning-ladder/
指定されたidのユーザーの学習中のladderのidのリストを返す
#### 結果
```
[
    {
        "id": 1
    },
    {
        "id": 4
    }
]
```
### GET users/:id/finish-ladder/
指定されたidのユーザーの学習済みのladderのリストを返す
#### 結果
```
[
    {
        "id": 2
    },
    {
        "id": 5
    }
]
```
---
### GET ladder/
公開状態がTrueのladderの一覧を返す
#### クエリパラエータ
|名前|型|必須|値の説明|
|:-|-|-|:-|
|limit|数値|　|何件取得するかの指定（指定なしは100件）|
|offset|数値||何件目から切り出すかの指定|
#### 結果
```
[
    "count": 6,
    "next": null,
    "previous": null
    {
        "id": 2,
        "title": "python",
        "is_public": true,
        "user": 2,
        "tags": [],
        "created_at": "2018-07-15T00:52:14.511474Z",
        "update_at": "2018-07-15T00:52:14.511501Z",
        "units": [],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 0,
        "count_finish_number": 0
    },
    {
        "id": 6,
        "title": "pythoon",
        "is_public": true,
        "user": 2,
        "tags": [],
        "created_at": "2018-07-15T11:37:40.463821Z",
        "update_at": "2018-07-15T11:37:40.463852Z",
        "units": [
            {
                "id": 6,
                "title": "Vue 2.0 Hello World",
                "description": "test",
                "ladder": 6,
                "url": "https://qiita.com",
                "index": 1
            },
            {
                "id": 4,
                "title": "test",
                "description": "test",
                "ladder": 6,
                "url": "https://aaa.com",
                "index": 3
            }
        ],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 0,
        "count_finish_number": 1
    },
    {
        "id": 1,
        "title": "pypython",
        "is_public": true,
        "user": 2,
        "tags": [
            3,
            4
        ],
        "created_at": "2018-07-14T15:59:51.940872Z",
        "update_at": "2018-07-16T07:55:06.557699Z",
        "units": [
            {
                "id": 3,
                "title": "python勉強",
                "description": "test",
                "ladder": 1,
                "url": "https://qiita.com",
                "index": 3
            },
            {
                "id": 2,
                "title": "pypython",
                "description": "test2",
                "ladder": 1,
                "url": "https://test.com",
                "index": 2
            },
            {
                "id": 1,
                "title": "pythoon",
                "description": "test",
                "ladder": 1,
                "url": "https://qiita.com",
                "index": 1
            }
        ],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 2,
        "count_finish_number": 0
    },
    {
        "id": 7,
        "title": "python入門",
        "is_public": true,
        "user": 3,
        "tags": [
            3
        ],
        "created_at": "2018-07-15T12:09:43.787345Z",
        "update_at": "2018-07-16T08:02:21.956610Z",
        "units": [],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 0,
        "count_finish_number": 0
    },
    {
        "id": 8,
        "title": "test",
        "is_public": true,
        "user": 2,
        "tags": [],
        "created_at": "2018-07-18T05:50:46.496288Z",
        "update_at": "2018-07-18T05:50:46.496309Z",
        "units": [
            {
                "id": 5,
                "title": "test",
                "description": "test",
                "ladder": 8,
                "url": "https://ladder.com",
                "index": 1
            }
        ],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 0,
        "count_finish_number": 0
    },
    {
        "id": 9,
        "title": "aaa",
        "is_public": true,
        "user": 2,
        "tags": [],
        "created_at": "2018-07-19T12:17:52.984974Z",
        "update_at": "2018-07-19T12:17:52.984995Z",
        "units": [],
        "recommended_prev_ladder": null,
        "recommended_next_ladder": null,
        "count_learning_number": 0,
        "count_finish_number": 0
    }
]
```
### POST ladder/
ladderの投稿
#### 認可
JWT認証が通ったユーザーのみ可能
ユーザーのidが`user`に登録される
#### 入力
|JSON key|型|必須|値の説明|
|:--|-|-|:-|
|title|文字列|○|ladderのタイトル|
|is_public|真偽値||公開状態 defaultはFalse|
|tags|数値||tagづけしたいtagのid|
|units|オブジェクト||unitのobjectのリスト　詳細は unit/へ|
#### 結果
```
{
    "id": 29,
    "title": "test337898r47899559",
    "is_public": true,
    "user": 2,
    "tags": [
        4,
        3
    ],
    "created_at": "2018-07-23T01:34:37.188578Z",
    "update_at": "2018-07-23T01:34:37.209490Z",
    "units": [],
    "recommended_prev_ladder": null,
    "recommended_next_ladder": null,
    "count_learning_number": 0,
    "count_finish_number": 0
}
```

### GET ladder/ranking/
学習者の多い上位5つのladderのidと学習者数を返す
#### 結果
```
[
    {
        "id": 1,
        "LearningNumber": 2
    },
    {
        "id": 2,
        "LearningNumber": 0
    },
    {
        "id": 3,
        "LearningNumber": 0
    },
    {
        "id": 4,
        "LearningNumber": 0
    },
    {
        "id": 5,
        "LearningNumber": 0
    }
]
```
### GET ladder/trend/
1週間以内に更新されたladderの中で学習者が多い上位5件のidと学習者数
#### 結果
```
[
    {
        "id": 1,
        "LearningNumber": 2
    },
    {
        "id": 2,
        "LearningNumber": 0
    },
    {
        "id": 3,
        "LearningNumber": 0
    },
    {
        "id": 4,
        "LearningNumber": 0
    },
    {
        "id": 5,
        "LearningNumber": 0
    }
]
```
---
### GET unit/
投稿されたunitの一覧
#### クエリパラエータ
|名前|型|必須|値の説明|
|:-|-|-|:-|
|limit|数値|　|何件取得するかの指定（指定なしは100件）|
|offset|数値||何件目から切り出すかの指定|
#### 結果
```
[
    "count": 6,
    "next": null,
    "previous": null
    {
        "id": 2,
        "title": "pypython",
        "description": "test2",
        "ladder": 1,
        "url": "https://test.com",
        "index": 2,
        "comments": null
    },
    {
        "id": 1,
        "title": "pythoon",
        "description": "test",
        "ladder": 1,
        "url": "https://qiita.com",
        "index": 1,
        "comments": null
    },
    {
        "id": 3,
        "title": "python勉強",
        "description": "test",
        "ladder": 1,
        "url": "https://qiita.com",
        "index": 3,
        "comments": null
    },
    {
        "id": 4,
        "title": "test",
        "description": "test",
        "ladder": 6,
        "url": "https://aaa.com",
        "index": 3,
        "comments": null
    },
    {
        "id": 5,
        "title": "test",
        "description": "test",
        "ladder": 8,
        "url": "https://ladder.com",
        "index": 1,
        "comments": null
    },
    {
        "id": 6,
        "title": "Vue 2.0 Hello World",
        "description": "test",
        "ladder": 6,
        "url": "https://qiita.com",
        "index": 1,
        "comments": null
    }
]
```

### POST unit/
unitの投稿
#### 認可
JWT認証が通ったユーザーのみ可能
#### 入力
|JSON key|型|必須|値の説明|
|:--|-|-|:--|
|title|文字列|○|unitのタイトル|
|description|文字列|○|説明文|
|ladder|数値|○|そのunitが所属するladder **ladder投稿時にまとめて投稿する時は自動でそのladderが代入される**|
|url|文字列(url)|○|そのサービスのurlまたは商品購入ページのurl|
|index|数値|○|所属するladderの中でのそのunitの順番|
#### 結果
```
{
    "id": 7,
    "title": "test",
    "description": "aaa",
    "ladder": 3,
    "url": "https://aaa.com",
    "index": 1,
    "comments": null
}
```

---
###  GET tag/
#### 結果
```
[
    {
        "id": 4,
        "name": "Django",
        "tagged_ladder_number": 2
    },
    {
        "id": 3,
        "name": "python",
        "tagged_ladder_number": 6
    }
]
```
---
### GET link/
pegの取得
#### 結果
```
[
    {
        "id": 1,
        "prior": 3,
        "latter": 4,
        "user": 2
    }
]
```
### POST link/
pegの投稿
#### 認可
JWT認証が通ったユーザーのみ可能
ユーザーのidが`user`に登録される
#### 入力
|JSON key|型|必須|値の説明|
|:-|-|-|:-|
|prior|数値|○|pegするときのprev_ladderのid|
|latter|数値|○|pegするときのnext_ladderのid|
#### 結果
```
{
    "id": 1,
    "prior": 3,
    "latter": 4,
    "user": 2
}
```
---
### GET learningstatus/
学習状況の一覧
#### 結果
```
[
    {
        "id": 1,
        "user": 2,
        "unit": 2,
        "status": true,
        "created_at": "2018-07-14T23:39:55.259558Z"
    },
    {
        "id": 2,
        "user": 2,
        "unit": 4,
        "status": true,
        "created_at": "2018-07-21T09:35:02Z"
    },
    {
        "id": 3,
        "user": 2,
        "unit": 1,
        "status": true,
        "created_at": "2018-07-21T10:36:31Z"
    },
    {
        "id": 6,
        "user": 3,
        "unit": 1,
        "status": true,
        "created_at": "2018-07-21T11:07:37Z"
    },
    {
        "id": 5,
        "user": 3,
        "unit": 2,
        "status": true,
        "created_at": "2018-07-21T11:06:48Z"
    },
    {
        "id": 4,
        "user": 2,
        "unit": 3,
        "status": false,
        "created_at": "2018-07-21T10:36:52Z"
    }
]
```
### POST learningstatus/
学習状況の登録
#### 認可
JWT認証が通ったユーザーのみ可能
ユーザーのidが`user`に登録される

#### 入力
|JSON key|型|必須|値の説明|
|:----|--|--|:--|
|unit|数値|○|unitのid|
|status|真偽値||学習済みかどうか  defaultはFalse|
#### 結果
```
{
    "id": 8,
    "user": 2,
    "unit": 5,
    "status": true,
    "created_at": "2018-07-23T03:04:42.443155Z"
}
```
---
### GET comments/
コメントの一覧
#### 結果
```
[
    {
        "id": 1,
        "unit": 2,
        "user": 2,
        "text": "aaaa",
        "target": null,
        "created_at": "2018-07-23T03:06:25Z"
    }
]
```
#### POST comments/
コメントの投稿
#### 認可
JWT認証が通ったユーザーのみ可能
ユーザーのidが`user`に登録される
#### 入力
|JSON key|型|必須|値の説明|
|:-|-|-|:-|
|unit|数値|○|コメントをつけたunitのid|
|text|文字列|○|コメント本文|
|target|数値||コメントに返信したときの返信先のコメントのid|
---
### POST　api-auth/
tokenの取得
#### 入力
|JSON key|型|必須|値の説明|
|:-------|--|--|-------|
|email|文字列|○|トークンを取得したいユーザーのメールアドレス|
|password|文字列|○|トークンを取得したいユーザーのパスワード|
