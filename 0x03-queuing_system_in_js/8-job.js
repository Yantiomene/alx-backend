function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw new Error('Jobs is not an array');
  jobs.forEach((data, index) => {
    let job = queue.create('push_notification_code_2', data);
      
      
    job
      .on('enqueue', () => {
        console.log(`Notification job created: ${job.id}`);
      })
      .on('complete', () => {
        console.log(`Notification job #${job.id} completed`);
      })
      .on('failed', (err) => {
        console.log(`Notification job #${job.id} failed: ${err}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job #${job.id} ${progress}% complete`)
      });
    job.save();
  });
}

export default createPushNotificationsJobs;
