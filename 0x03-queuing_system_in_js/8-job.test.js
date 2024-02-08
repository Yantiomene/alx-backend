import assert from 'assert';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function() {
  let queue;

  beforeEach(function() {
    queue = kue.createQueue({ redis: { createClientFactory: kue.redisClientFactory } });
    queue.testMode.enter();
  });

  afterEach(function(done) {
    queue.testMode.clear();
    queue.testMode.exit();
    done();
  });

  it('should create jobs in the queue and display an error message if jobs is not an array', function() {

      assert.throws(() => {
	createPushNotificationsJobs('not an array', queue);
      }, { message: 'Jobs is not an array' });
  });

  it('should log job creation, completion, failure, and progress', function(done) {
    const jobs = [
      { phoneNumber: '1111111111', message: 'Test message 1' },
      { phoneNumber: '2222222222', message: 'Test message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    setTimeout(() => {
      assert.equal(queue.testMode.jobs.length, jobs.length);
      queue.testMode.jobs[0].emit('failed', new Error('Job failed'));
      queue.testMode.jobs[1].emit('complete');
      queue.testMode.jobs[1].emit('progress', 50);

      setTimeout(() => {
        done();
      }, 1000);
    }, 500);
  });
});
