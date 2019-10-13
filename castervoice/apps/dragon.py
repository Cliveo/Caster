from dragonfly import Function, Playback, Mimic, WaitWindow, Repeat, Pause
from castervoice.lib.actions import Key
from castervoice.lib.context import AppContext

from castervoice.apps.dragon_support import cap_dictation, fix_dragon_double, extras_for_whole_file, \
    defaults_for_whole_file
from castervoice.lib import utilities
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class DragonRule(MergeRule):
    pronunciation = "dragon"

    mapping = {
        "format <text>": Function(cap_dictation, extra={"text"}),
        '(lock Dragon | deactivate)':
            R(Playback([(["go", "to", "sleep"], 0.0)])),
        '(number|numbers) mode':
            R(Playback([(["numbers", "mode", "on"], 0.0)])),
        'spell mode':
            R(Playback([(["spell", "mode", "on"], 0.0)])),
        'dictation mode':
            R(Playback([(["dictation", "mode", "on"], 0.0)])),
        'normal mode':
            R(Playback([(["normal", "mode", "on"], 0.0)])),
        '(command mode | command on | com on)':
            R(Playback([(["command", "mode", "on"], 0.0)])),
        '(command off | com off)':
            R(Playback([(["command", "mode", "off"], 0.0)])),
        "reboot dragon":
            R(Function(utilities.reboot)),
        "fix dragon double":
            R(Function(fix_dragon_double)),
        "left point":
            R(Playback([(["MouseGrid"], 0.1), (["four", "four"], 0.1),
                        (["click"], 0.0)])),
        "right point":
            R(Playback([(["MouseGrid"], 0.1), (["six", "six"], 0.1), (["click"], 0.0)])),
        "center point":
            R(Playback([(["MouseGrid"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Center Point"),
        
        
        "show windows": R(Mimic("list", "all", "windows"),  
            rdescript="Dragon: emulate Dragon command for listing windows"),
        "cory <text>": 
            R(Mimic("correct", extra="text") + WaitWindow(title="spelling window") + Mimic("choose", "one"),
                rdescript="Dragon: brings up the correction menu for the phrase spoken in the command and chooses the 1st choice"),
        "cory that": 
            R(Mimic("correct", "that") + WaitWindow(title="spelling window") + Mimic("choose", "one"), 
                rdescript="Dragon: brings up the correction menu for the previously spoken phrase and chooses the first choice"),

        "make that <text>": R(Mimic("scratch", "that") + Mimic(extra="text"), 
             rdescript="Dragon: deletes the dictation generated by the previous utterance and replaces it with what you say next"),
        "scratch [<n10>]": R(Playback([(["scratch", "that"], 0.03)]), 
            rdescript="Dragon: delete dictation from previous n utterances") * Repeat(extra="n10"),

            # Users may want to adjust the wait time on the next few commands     
        "train word": R(Mimic("train", "that") + Pause("75") + Key("a-r/250, s"),
             rdescript="Dragon: quickly train word when you have it selected in a Dragon friendly text field"),
        "word train": R(Key("c-c/20") + Mimic("edit", "vocabulary") + 
            Key("c-v/5, tab, down, up, a-t/50, enter/50, a-r/250, s/50, escape"),
             rdescript="train word quickly once you have it selected in non-full text control application"),
        "(add train | train from add word)": R(Key("a-a/2, enter/300, a-s"),
            rdescript="Dragon: quickly train word from the add word dialogbox"),
    
        "(train from vocab | cab train)": R(Key("a-t/50, enter/50, a-r/250, s"), 
            rdescript="Dragon: quickly train word from Vocabulary Editor"),
        "(train from vocab | cab train)": R(Key("a-t/50, enter/50, a-r/250, s"), 
            rdescript="Dragon: quickly train word from Vocabulary Editor"),
        "remove from vocab":
            R(Key("c-c/5") + Mimic("edit", "vocabulary") + Pause("20") + 
            Key("c-v/10, tab, down, up/5, a-d, y, escape/30, right"), 
            rdescript="Dragon: remove selected word from vocabulary"),
        "(add to vocab | vocab that)":
            R(Key("c-c/5") + Mimic("add", "word") + Pause("20") +
            Key("c-v, a-a/2, enter/300, a-s/30, right"),
            rdescript="Dragon: add selected word to vocabulary and train it"),

        "recognition history": 
            R(Playback([(["view", "recognition", "history"], 0.03)]),
             rdescript="Dragon: open Dragon recognition history"),
        "peak [recognition] history": 
            R(Playback([(["view", "recognition", "history"], 0.03)])
                + Pause("300") + Key("escape"), 
                    rdescript="Dragon: open Dragon recognition history then close it"),
        "[dictation] sources": R(Mimic("manage", "dictation", "sources"), 
            rdescript="Dragon: manage dictation sources"),
        

        # A Natlink Command
        "clear caster log":
            R(Function(utilities.clear_log)),
    }
    # see above
    extras = extras_for_whole_file()
    defaults = defaults_for_whole_file()


def get_rule():
    return DragonRule, RuleDetails(name="dragon")
