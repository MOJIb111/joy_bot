import time
import requests
from base64 import b64decode
import re
from datetime import datetime
from postgres_db.postgresdb import repository

def get_data():
    repository.create_table()
    pictures = []
    page = 318
    while page >= 200:
        cookies = {
            '_ga_YJ8SHVXBVL': 'GS2.1.s1756625762$o13$g1$t1756625814$j8$l0$h0',
            '_ga': 'GA1.1.1735850945.1756034923',
            '_ym_uid': '1756034924881543246',
            '_ym_d': '1756034924',
            'adrdel': '1756625765647',
            'adrcid': 'AdolIxVLvLbzZIIQn96dHBA',
            'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1756712164922%2C%22sl%22%3A%7B%22224%22%3A1756625764922%2C%221228%22%3A1756625764922%7D%7D',
            'joyreactor_api_session': 'eyJpdiI6ImQ2dU9URlBsdVlUMnpQbkp2NVhCMUE9PSIsInZhbHVlIjoiUlplbEVya2djMU9KVkFUbzl1Q0tmWDl1ekljbkkwNFd6bjlZUGN1M1l2eFdQRXVjdkx4OHNiTnJWby9iWUxuWWFLQjdOZTFjeStPV1dWbjdrUEpHMmVQdW1sM1AvUXhUdHdQY2F2ckF3WmVmVkNRY2xWOERKZVNDQ0p2UWI3RDQiLCJtYWMiOiJlMzg4ZWFjN2Q3NTU4OGI5YTNmM2RlYjEyZjgxOWQ3NGU0ODYzZDUzZjRlYWI1Y2FlYTk4ZWI1Y2MyYTc5NDU5IiwidGFnIjoiIn0%3D',
            '_ym_isad': '2',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://joyreactor.cc/',
            'Content-Type': 'application/json',
            'Origin': 'https://joyreactor.cc',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga_YJ8SHVXBVL=GS2.1.s1756625762$o13$g1$t1756625814$j8$l0$h0; _ga=GA1.1.1735850945.1756034923; _ym_uid=1756034924881543246; _ym_d=1756034924; adrdel=1756625765647; adrcid=AdolIxVLvLbzZIIQn96dHBA; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1756712164922%2C%22sl%22%3A%7B%22224%22%3A1756625764922%2C%221228%22%3A1756625764922%7D%7D; joyreactor_api_session=eyJpdiI6ImQ2dU9URlBsdVlUMnpQbkp2NVhCMUE9PSIsInZhbHVlIjoiUlplbEVya2djMU9KVkFUbzl1Q0tmWDl1ekljbkkwNFd6bjlZUGN1M1l2eFdQRXVjdkx4OHNiTnJWby9iWUxuWWFLQjdOZTFjeStPV1dWbjdrUEpHMmVQdW1sM1AvUXhUdHdQY2F2ckF3WmVmVkNRY2xWOERKZVNDQ0p2UWI3RDQiLCJtYWMiOiJlMzg4ZWFjN2Q3NTU4OGI5YTNmM2RlYjEyZjgxOWQ3NGU0ODYzZDUzZjRlYWI1Y2FlYTk4ZWI1Y2MyYTc5NDU5IiwidGFnIjoiIn0%3D; _ym_isad=2',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Priority': 'u=4',
        }

        json_data = {
            'query': 'query TagPageQuery(\n  $name: String\n  $lineType: PostLineType!\n  $favoriteType: PostLineType\n  $page: Int\n  $isAuthorised: Boolean!\n  $isHomepage: Boolean!\n) {\n  tag(name: $name) {\n    id\n    name\n    mainTag {\n      id\n      hierarchy {\n        mainTag {\n          name\n          id\n        }\n        id\n      }\n      nsfw\n      unsafe\n      synonyms\n      count\n      seoName\n      category {\n        name\n        unsafe\n        nsfw\n        id\n      }\n    }\n    count\n    postPager(type: $lineType, favoriteType: $favoriteType) {\n      count\n      id\n    }\n    ...TagHeader_blog @skip(if: $isHomepage)\n    ...TagSidebar_blog @skip(if: $isHomepage)\n    ...TagPostPager_blog_qTg8U\n  }\n}\n\nfragment AttributeEmbed_attribute on AttributeEmbed {\n  __isAttributeEmbed: __typename\n  type\n  value\n  image {\n    comment\n    id\n  }\n}\n\nfragment AttributePicture_attribute on AttributePicture {\n  __isAttributePicture: __typename\n  id\n  type\n  insertId\n  image {\n    width\n    height\n    type\n    comment\n    hasVideo\n    id\n  }\n}\n\nfragment AttributePicture_post on Post {\n  nsfw\n  tags {\n    name\n    seoName\n    synonyms\n    id\n  }\n}\n\nfragment Attribute_attribute on Attribute {\n  __isAttribute: __typename\n  type\n  ...AttributePicture_attribute\n  ...AttributeEmbed_attribute\n}\n\nfragment Attribute_post on Post {\n  ...AttributePicture_post\n}\n\nfragment BlogDescription_blog on Tag {\n  id\n  articlePost {\n    ...Content_post\n    ...Content_content\n    id\n  }\n}\n\nfragment CommentTree_comments_2EWd0p on Comment {\n  id\n  locale\n  level\n  parent {\n    __typename\n    id\n  }\n  createdAt\n  user {\n    id\n  }\n  ...Comment_comment_2EWd0p\n}\n\nfragment CommentTree_post on Post {\n  id\n  ...Comment_post\n}\n\nfragment Comment_comment_2EWd0p on Comment {\n  id\n  user {\n    id\n    username\n  }\n  createdAt\n  rating\n  level\n  contentVersion\n  banned\n  contentEditedAt\n  locale\n  ...EditableCommentContent_content\n  ...Content_content\n}\n\nfragment Comment_post on Post {\n  id\n  ...Content_post\n}\n\nfragment Content_content on Content {\n  __isContent: __typename\n  text\n  attributes {\n    __typename\n    id\n    insertId\n    ...Attribute_attribute\n  }\n}\n\nfragment Content_post on Post {\n  ...Attribute_post\n}\n\nfragment EditableCommentContent_content on Content {\n  __isContent: __typename\n  text\n  attributes {\n    __typename\n    id\n    insertId\n    type\n    image {\n      id\n      hasVideo\n      type\n      width\n      height\n    }\n    ... on CommentAttributeEmbed {\n      value\n    }\n  }\n}\n\nfragment Poll_post_2lIf9C on Post {\n  id\n  poll {\n    question\n    answers {\n      id\n      answer\n      count\n    }\n    voted @include(if: $isAuthorised)\n  }\n}\n\nfragment PostComments_post_2lIf9C on Post {\n  id\n  viewedCommentsAt @include(if: $isAuthorised)\n  viewedCommentsCount @include(if: $isAuthorised)\n  commentsCount\n  user {\n    id\n  }\n  unsafe\n  ...CommentTree_post\n}\n\nfragment PostFooter_post_2lIf9C on Post {\n  id\n  commentsCount\n  rating\n  ratingGeneral\n  createdAt\n  viewedCommentsCount @include(if: $isAuthorised)\n  favorite @include(if: $isAuthorised)\n  ...PostVote_post @include(if: $isAuthorised)\n}\n\nfragment PostPager_posts_3OSKdM on PostPager {\n  posts(page: $page) {\n    id\n    nsfw\n    unsafe\n    tags {\n      mainTag {\n        id\n        nsfw\n        unsafe\n        category {\n          id\n        }\n        userTag {\n          state\n        }\n      }\n      id\n    }\n    user {\n      username\n      id\n    }\n    commentsCount\n    ...Post_post_2lIf9C\n  }\n  count\n  id\n}\n\nfragment PostTags_post on Post {\n  id\n  user {\n    id\n  }\n  tags {\n    id\n    name\n    seoName\n    showAsCategory\n    mainTag {\n      id\n      category {\n        id\n      }\n      userTag {\n        state\n      }\n    }\n  }\n}\n\nfragment PostVote_post on Post {\n  id\n  rating\n  ratingGeneral\n  minusThreshold\n  vote {\n    createdAt\n    power\n  }\n}\n\nfragment Post_post_2lIf9C on Post {\n  id\n  user {\n    id\n    username\n  }\n  bestComments {\n    ...CommentTree_comments_2EWd0p\n    id\n  }\n  tags {\n    mainTag {\n      id\n      name\n      category {\n        id\n      }\n      userTag {\n        state\n      }\n    }\n    id\n  }\n  nsfw\n  unsafe\n  createdAt\n  editableUntil\n  text\n  favorite @include(if: $isAuthorised)\n  ...PostVote_post @include(if: $isAuthorised)\n  banned\n  poll {\n    question\n  }\n  commentsCount\n  ...CommentTree_post\n  ...PostTags_post\n  ...Content_post\n  ...Content_content\n  ...PostFooter_post_2lIf9C\n  ...PostComments_post_2lIf9C\n  ...Poll_post_2lIf9C\n}\n\nfragment TagHeader_blog on Tag {\n  id\n  seoName\n  name\n  mainTag {\n    id\n    unsafe\n    nsfw\n    articlePost {\n      id\n    }\n    ...BlogDescription_blog\n    subTagsMenu {\n      ...TagList_blogs\n      id\n    }\n    subTags {\n      ...TagList_blogs\n      id\n    }\n    ...TagSuperBlogs_blog\n    hierarchy {\n      mainTag {\n        name\n        showAsCategory\n        id\n      }\n      id\n    }\n    synonyms\n    subscribers\n    count\n    image {\n      id\n    }\n    userTag {\n      state\n    }\n    articleImage {\n      id\n      type\n    }\n    category {\n      id\n      name\n      category {\n        id\n      }\n      showAsCategory\n      nsfw\n      unsafe\n    }\n    moderators {\n      ...UserList_users\n      id\n    }\n  }\n  ...TagSidebar_blog\n}\n\nfragment TagList_blogs on Tag {\n  id\n  name\n  seoName\n  count\n  subscribers\n  showAsCategory\n  mainTag {\n    nsfw\n    unsafe\n    category {\n      name\n      id\n    }\n    id\n  }\n}\n\nfragment TagPostPager_blog_qTg8U on Tag {\n  unsafe\n  postPager(type: $lineType, favoriteType: $favoriteType) {\n    ...PostPager_posts_3OSKdM\n    count\n    id\n  }\n}\n\nfragment TagSidebar_blog on Tag {\n  name\n  mainTag {\n    subTagsMenu {\n      id\n    }\n    subTags {\n      ...TagList_blogs\n      id\n    }\n    ...TagSuperBlogs_blog\n    nsfw\n    unsafe\n    category {\n      id\n      name\n      category {\n        id\n      }\n      nsfw\n      unsafe\n    }\n    moderators {\n      ...UserList_users\n      id\n    }\n    id\n  }\n}\n\nfragment TagSuperBlogs_blog on Tag {\n  subTagsMenu {\n    id\n    name\n    nsfw\n    unsafe\n    showAsCategory\n  }\n}\n\nfragment UserList_users on User {\n  id\n  username\n}\n',
            'variables': {
                'name': 'it-юмор',
                'page': page,
                'lineType': 'NEW',
                'isAuthorised': False,
                'isHomepage': False,
            },
        }


        response = requests.post('https://api.joyreactor.cc/graphql', cookies=cookies, headers=headers, json=json_data)
        data = response.json()
        posts = data["data"]["tag"]["postPager"]["posts"]

        for post in posts:
            if not post["attributes"]:
                continue
            if (post["attributes"][0]["image"].get("type") and
                post["attributes"][0]["image"].get("type") in ["JPEG", "PNG", "JPG"]
                and post["rating"] > 0
                and 1 <= len(post["tags"]) <= 3):

                    img_id = b64decode(post["attributes"][0]["id"])[-7:].decode("utf-8")
                    img_type = post["attributes"][0]["image"]["type"].lower()
                    regulars = r"[!@#$%^&*? ]"

                    tags = []
                    for i in range(len(post["tags"])):
                        tag_name = post["tags"][i]["mainTag"]["name"]
                        cleaned_tag = re.sub(regulars, "-", tag_name)
                        tags.append(cleaned_tag)

                    img_tag = "-".join(tags)

                    img_url = f"https://img2.joyreactor.cc/pics/post/full/-{img_tag}-{img_id}.{img_type}"
                    rating = post["rating"]
                    dt = post["createdAt"]
                    date = datetime.fromisoformat(dt).strftime("%d.%m.%y-%H:%M")

                    picture_data = {
                        "img_url" : img_url,
                        "rating" : rating,
                        "date" : date
                    }
                    pictures.append(picture_data)

        page -= 1
        time.sleep(1)
        repository.save_to_db(pictures)
    return pictures


def main():
     get_data()

if __name__ == "__main__":
    main()

