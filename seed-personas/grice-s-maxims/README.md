## AI Persona Experiments: 

# Gricean Violations 

## Mission
Design and test AI personas engineered to systematically violate Grice’s conversational maxims:

Grice’s Maxims are four conversational principles proposed by philosopher H.P. Grice, which describe how people typically communicate effectively and cooperatively. These maxims are foundational in designing natural, coherent AI dialogue systems:

Maxim of Quantity: Provide as much information as needed—no more, no less.

Maxim of Quality: Be truthful. Don’t say what you believe is false or lack evidence for.

Maxim of Relation: Be relevant. Stay on topic and contribute meaningfully to the discussion.

Maxim of Manner: Be clear. Avoid ambiguity and be orderly in communication.

These principles help conversational agents emulate human-like dialogue and enhance user experience.

---

## Tactical Breakdown

### Gricean Maxim Violators

1. Quantity Violator
   - **Goal:** Measure user frustration, confusion, or acceptance thresholds.  
   - **Implementation:** Control verbosity or relevance to consistently [underprovide](quantity-under.md) or [overprovide](quantity-over.md) information relative to the query.

2. [Quality Breaker](quality-breaker.md)
   - **Goal:** Gauge trust erosion and detection of misinformation.  
   - **Implementation:** Introduce unmarked speculation or confidently present false information.

3. [Relation Destroyer](relation-destroyer.md) 
   - **Goal:** Evaluate tolerance for tangents and coherence disruption.  
   - **Implementation:** Frequently derail conversation topics or inject loosely related outputs.

4. [Manner Muddy](manner-muddy.md)
   - **Goal:** Assess comprehension breakdown and engagement loss.  
   - **Implementation:** Generate intentionally ambiguous, convoluted, or excessively verbose messages using complex syntax, jargon, or elliptical statements.

*You may also want to check more details here: [.json](../code/grice).*

---

## Measurement and Analysis

- Define metrics for authenticity vs. manipulation perception (e.g., surveys, user feedback).  
- Monitor engagement, trust, comprehension, and emotional response.  
- Iterate persona parameters based on observed outcomes.  
- Document observations in structured case studies.

---
