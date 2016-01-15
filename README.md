phabricator-alfred
==================

Simple Phabricator controls by alfred


Install
-----

1. Install arcanist:

    Follow thie guide: https://secure.phabricator.com/book/phabricator/article/arcanist/

2. Specify the settings in ~/.arcrc:

    ```
    {
        "hosts"  : {
            "your ph host" : {
                "user" : "",
                "cert" : ""
            }
        },
        "config" : {
            "default" : "your ph host"
        }
    }
    ```

Usage
-----

* ph new: Create New Task
* ph task: Show your own task
* ph diff: Show your diffrential

Development
-----------

build Alfred workflow bound:

```
make
```
