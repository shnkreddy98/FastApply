document.getElementById('submitButton').addEventListener('click', async () => {
  const jobDescription = document.getElementById('jobDescription').value;

  if (!jobDescription) {
    alert('Please enter a job description.');
    return;
  }

  try {
    const response = await fetch('/process', {  // Changed the URL to be relative
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ job_description: jobDescription }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
  }
});