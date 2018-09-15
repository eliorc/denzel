API Endpoints
=============

| Denzel exposes three different endpoints for end users.
| All endpoints are relative to the host. For example if deployed locally on the default port the endpoint ``/info`` means ``localhost:8000/info``


.. contents:: Endpoints
    :local:

.. _`info_endpoint`:

-----
/info
-----

.. http:get:: /info

    Endpoint for deployment information. Basically returns the content of ``app/assets/info.txt``.


.. _`predict_endpoint`:

--------
/predict
--------

.. http:post:: /predict

    Endpoint for performing predictions

    :reqheader Accept: application/json
    :form body: Data necessary for prediction, should match the interface defined

    :status 200: Request accepted and entered the task queue
    :status 400: Failed to in the reading / verification process.


.. _`status_endpoint`:

-----------------
/status/{task_id}
-----------------

.. http:get:: /status/(str:task_id)

    Endpoint for checking a task status

    :param task_id: Task ID

