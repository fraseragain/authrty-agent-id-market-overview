# Chain rubric, general actions variant

The [chain rubric](chain-rubric.md) was written with a purchase in mind: amounts, payees, receipts, chargebacks. Most of what an agent does for someone is not a purchase. This variant keeps the same ten links and scoring (2 met, 1 partial, 0 absent; chain score = weakest link) but rewrites the tests that assume money, so that a protocol is judged on whether the chain holds for *any* consequential action.

Links L1, L2, L3, L9 and L10 are unchanged. A payment-only mechanism (amount limits, payment receipts, chargebacks) scores nothing in this variant unless the same mechanism also covers non-payment actions.

## Action classes

Score which classes a protocol's grant and evidence can explicitly express. Each class scores yes (the spec defines how a grant or record covers it), partial (it is possible through a generic mechanism such as an OAuth scope or tool name, with no defined semantics), or no.

| Class | Examples |
|---|---|
| A. Read or retrieve data | Read a mailbox, fetch account history, query a record |
| B. Communicate on the principal's behalf | Send an email or message, post, reply to a company's agent |
| C. Change state in an account | Book or cancel, change settings, update an address, submit a form |
| D. Legally significant act | Accept terms, give consent, sign, submit an application or claim |
| E. Pay | Purchase, transfer, subscribe |
| F. Delegate onward | Instruct another agent to act |

## Rewritten tests

**L4 Delegation**
- D2 (rewritten). The grant can constrain *what* may be done: the operation or tool, the resource or account, the data scope, the recipient or counterparty, a count or rate, and a time window. Amount and payee alone are partial.

**L5 Session authentication**
- S3 (rewritten). The protocol defines a step-up for high-risk actions of *any* class: re-confirmation by the human, with an assurance level, before the action. Payment-only step-up (for example 3-D Secure) is partial.

**L6 Action conformance**
- A1 (rewritten). The request for an action references the grant it relies on, for non-payment actions as well as payments.
- A2 (rewritten). Before acting, the counterparty can check that *this operation on this resource* falls within the grant. A scope-only check is partial.

**L7 Evidence**
- E1 (rewritten). A record of the action says what was done, to which resource, and with what inputs. It is signed by an identifiable, accountable party: the agent, the acting server, or both.
- E4 (new). The *outcome* is evidenced: the counterparty's response or result is signed, so both sides can later prove what the other did.
- E2 and E3 are unchanged.

**L8 Redress**
- R1 (rewritten). Responsibility for an unauthorised or mistaken action is allocated between named roles. This covers harm that is not monetary: data disclosed, a message sent, an account changed.
- R2 (rewritten). There is a path to contest, reverse or remedy an action, such as cancel, roll back, revoke a consent or report an incident, defined natively or by reference to a named rulebook. Chargebacks alone score 0.
