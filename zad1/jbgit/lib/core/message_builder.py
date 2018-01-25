# simple output message constructing functions

import re


class MessageBuilder:
    def __init__(self):
        pass

    def build_init_message (self, message_template, repo_path):
        return message_template + " in directory " + repo_path

    # returns message from message template combined with specific counter
    def build_xmessage(self, message_template, x):
        return "Nothing to do for zero files." if x == 0 else re.sub("X", str(x), message_template)

    # builds status output message
    def build_status(self, message_template, added, new, modified):
        strlist = [message_template]
        if len(added)+len(new)+len(modified) > 0:
            for afile in added:
                strlist.append(afile+" (staged file)")
            for mfile in modified:
                strlist.append(mfile+" (modified file)")
            for nfile in new:
                strlist.append(nfile+" (new file)")
        else:
            strlist.append("No changes detected.")

        return ('\n'.join(strlist))