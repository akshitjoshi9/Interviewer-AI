const interviewId = localStorage.getItem("interview_id");

async function loadResults() {
   const res = await fetch(`/api/interview/${interviewId}/results`);
   const data = await res.json();

   if (data.status !== "ok") return;
   const percentage = parseFloat(data.summary.percentage) || 0;

   const decision = percentage >= 50 ? "Pass" : "Fail";
   const decisionClass = decision === "Pass" ? "pass" : "danger";

   // SUMMARY
   document.getElementById("summary").innerHTML = `
       <div class="summary-card">
           <h4>Total Score</h4>
           <div class="big">${data.summary.total_score}/${data.summary.max_score}</div>
       </div>

       <div class="summary-card">
           <h4>Percentage</h4>
           <div class="big">${percentage}%</div>
       </div>

       <div class="summary-card ${decisionClass}">
           <h4>Final Decision</h4>
           <span class="decision-pill ${decisionClass}">
               ${decision.toUpperCase()}
           </span>
       </div>
   `;

   // QUESTIONS
   const resultsEl = document.getElementById("results");
   resultsEl.innerHTML = "";

   data.results.forEach((r, i) => {
       resultsEl.innerHTML += `
           <div class="qa-card">

               <div class="qa-header">
                   <span class="q-no">Q${i + 1}</span>
                   <h3>${r.question}</h3>
                   <span class="score-badge">${r.score} / 10</span>
               </div>

               <div class="qa-body">
                   <div class="answer">
                       <h4>Candidate Answer</h4>
                       <p>${r.answer || "No response given"}</p>
                   </div>

                   <div class="feedback">
                       <h4>AI Feedback</h4>
                       <p>${r.feedback}</p>
                   </div>
               </div>

           </div>
       `;
   });
}

loadResults();
