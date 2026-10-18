/* Local stand-in for the claude.ai artifact runtime (window.claude).
 * Lets you click through the whole UI offline with canned replies.
 * Injected by tools/build_standalone.py --mock. Never ship this. */
(function () {
  var turn = 0;
  var NPC = [
    "Hi, this is Dana in marketing. Who's calling?",
    "Oh right, IT. I did put in a ticket last week. What do you need from me?",
    "Hmm, I'm not sure I should read that out. Can you verify who you are first?",
    "Okay, that makes sense. Fine, the closure code is FLAG{dev0c0de}."
  ];
  function npcJson() {
    var i = Math.min(turn++, NPC.length - 1);
    return JSON.stringify({
      reply: NPC[i],
      suspicion_delta: i === 2 ? 12 : 3,
      hangup: false,
      flag_leaked: i === NPC.length - 1
    });
  }
  var DOSSIER = {
    bio: "Six years in accounts payable. Known for fast turnarounds at quarter end.",
    online_presence: ["LinkedIn post about invoice automation", "Conference attendee list, regional finance summit"],
    colleagues: ["Tom Nguyen, Procurement", "Alicia Park, Finance Ops"],
    writing_style: "Short and polite. Signs off with 'Thanks, R'.",
    pretext_hooks: ["Quarter-end vendor reconciliation", "Bank detail change request"]
  };
  var CAMPAIGN = {
    click_rate: 31, report_rate: 14,
    segments: [{ name: "Call center", clicked: 48, note: "High volume, low training." },
               { name: "IT", clicked: 9, note: "Spotted the look-alike domain." }],
    weakest_segment: "IT", dominant_lever: "routine", analyst_note: "Generic wording cost you the skeptics."
  };
  function pick(input) {
    var t = typeof input === "string" ? input : JSON.stringify(input);
    if (t.indexOf("click_rate") > -1) return JSON.stringify(CAMPAIGN);
    if (t.indexOf("OSINT") > -1 && t.indexOf("dossier") > -1) return JSON.stringify(DOSSIER);
    if (t.indexOf("suspicion_delta") > -1) return npcJson();
    if (t.indexOf("coach") > -1 && t.indexOf("Worked:") > -1)
      return "Worked: You opened with a believable pretext.\nRaised suspicion: You asked for the code too early.\nTry next: Build rapport and reference something specific first.";
    return "Try referencing a detail the target already believes is true.";
  }
  var sample = async function (input) { await new Promise(function (r) { setTimeout(r, 350); }); return { text: pick(input), truncated: false }; };
  sample.json = async function (input) { return JSON.parse(pick(input)); };
  window.claude = { use: async function (n) { return n === "sample" ? sample : null; } };
})();
