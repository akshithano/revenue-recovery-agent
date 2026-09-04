# Revenue Recovery Agent

This is a submission for Razorpay's Buildathon, AI Revenue Recovery track.

The idea: when a payment fails or someone abandons checkout, most of that revenue just quietly disappears. This is a small agent that looks at a batch of failed/abandoned transactions, figures out why each one failed, and decides what to do about it: retry it, nudge the customer, or hand it off to a human. Every decision gets logged with a reason, so nothing happens silently.

The decision logic is plain rules, not AI. I kept it that way on purpose. I didn't want the system guessing at what to do with someone's money. The only place AI shows up is writing the actual message a customer would see, which felt like a reasonable place for it since that's a language task, not a decision.

## How it works

Each transaction gets checked against a few rules:

- If it's already been retried twice, stop. Hand it to a human instead of hammering the customer again.
- If the failure looks temporary (bank timeout, insufficient funds), retry it.
- If the card's expired, retrying won't help, so it asks the customer to update their payment method instead.
- If it's an abandoned checkout, send a gentle reminder.
- If none of that matches, don't guess. Escalate.

For the "nudge" cases, it calls an LLM (running on Groq, using an open model called gpt-oss-120b) to write a short, natural message. If that call fails for any reason (no API key, network hiccup, empty response), it falls back to a plain template message instead of crashing the whole run.

Everything gets written to `audit_trail.csv`, along with a summary of how much was recovered vs. how much was at risk.

There's also a `dashboard.html` you can generate from the audit trail. Mostly just a nicer way to look at the same numbers.

## Running it

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# open .env and add your own GROQ_API_KEY (free, no card needed)
# it'll still run without one, just with plainer messages

python generate_data.py
python main.py
python generate_dashboard.py   # optional, opens dashboard.html in a browser
```

## What's real and what's not

The transactions are synthetic. I made them up, not pulled from a real merchant. The retry/nudge "success rates" are also just fixed probabilities standing in for how a real payment gateway would behave. The decision logic and the AI message generation are both real and actually run.

## One run, for reference

60 transactions, about Rs 4.87 lakh at risk, ~47.5% recovered, 10 escalated to a human instead of being retried past the limit.

## Files

- `generate_data.py`: makes the fake transaction batch
- `rules_engine.py`: the actual decision logic and the hard limits
- `simulate_execution.py`: fakes the outcome of a retry/nudge
- `ai_messenger.py`: calls Groq to write the customer message, with a fallback
- `main.py`: runs everything, builds the audit trail
- `generate_dashboard.py`: builds the html report
## Built with

* **Python 3** & **Groq API** (`openai/gpt-oss-120b`) for personalized customer messaging.
* **Claude AI** for rapid prototyping, synthetic data generation, and dashboard layout design.
