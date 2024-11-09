#!/usr/bin/env python3

import os
import re
from subprocess import Popen, PIPE

os.chdir("/tmp/")

with open("FormResponse.txt", "r") as f:
    contents = f.read()

    name = re.compile(r"(Name:)\ (\w+).*")
    name_matches = name.finditer(contents)

    for match in name_matches:
        name = match.group(2)

    email = re.compile(r"(Email:)\ (.*)")
    email_matches = email.finditer(contents)

    for match in email_matches:
        email = match.group(2)

    subject = re.compile(r"(Subject:)\ (.*)")
    subject_matches = subject.finditer(contents)

    for match in subject_matches:
        subject = "Re: " + match.group(2)


script = """
tell application "Mail"

	set theFrom to "contact@matthammond.com"
	set theTo to "%s"
    set theSubject to "Re: %s"
	set theContent to "%s,

Thanks for reaching out through my website. I'll be sure to check your message and get back to you promptly with any information or assistance you need."

    set theMessage to make new outgoing message with properties {sender:theFrom, subject:theSubject, content:theContent, message signature:(signature named "FormResponse"), visible:true}
    ---
    tell theMessage
		make new to recipient at end of to recipients with properties {address:theTo}
	end tell
    ---
	send theMessage
	-- save theMessage
end tell""" % (email, subject, name)

p = Popen(
    ["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True
)
stdout, stderr = p.communicate(script)
