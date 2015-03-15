all: ph

ph:
	zip -r9 --filesync phabricator.alfredworkflow *{plist,png,py} workflow phabricator -x *pyc
