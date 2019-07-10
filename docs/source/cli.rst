Command Line Interface (CLI)
============================

| Denzel comes with a CLI for the developers use.
| At any moment you can use the ``--help`` flag to see the help menu

.. code-block:: bash

    $ denzel --help

    Usage: denzel [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      launch         Builds and starts all services
      logs           Show service logs
      logworker      Show worker log
      response       Set response manner (sync/async) and sync timeout
      restart        Restart services
      shell          Connect to service bash shell
      shutdown       Stops and deletes all services
      start          Start services
      startproject   Builds the denzel project skeleton
      status         Examine status of services and worker
      stop           Stop services
      updateosreqs   Run shell commands from requirements.sh on all services
      updatepipreqs  Update services according to requirements.txt
      updatereqs     Update services using requirements.txt and requirements.sh


| For command specific help you can follow a command with the ``--help`` flag (ex. ``denzel launch --help``)


.. contents:: Commands
    :local:
    :depth: 1

.. note::
    Except from the :ref:`startproject` command, all other commands must be executed from within project directory


.. _startproject:

----------------
``startproject``
----------------

Usage: ``denzel startproject NAME``

Builds the denzel project skeleton.

.. py:attribute:: NAME

    Name of the project

.. option:: --gpu|--no-gpu

    Support for NVIDIA GPU

    Default: ``--no-gpu``

++++++++
Examples
++++++++

 - Start a project named "iris_classifier" with the default CPU image

    .. code-block:: bash

        $ denzel startproject iris_classifier

 - Start a project named "iris_classifier" with a GPU image

    .. code-block:: bash

        $ denzel startproject --gpu iris_classifier


.. _launch:

----------
``launch``
----------

Usage: ``denzel launch [OPTIONS]``

Builds and starts all services.

.. option:: --api-port <INTEGER>

    API endpoints port

    Default: ``8000``

.. option:: --monitor-port <INTEGER>

    Monitor UI port

    Default: ``5555``

++++++++
Examples
++++++++

 - Launch project with the default ports (8000 for API and 5555 for monitoring)

    .. code-block:: bash

        $ denzel launch

 - Launch a project with 8080 as the API port

    .. code-block:: bash

        $ denzel launch --api-port 8080


.. _shutdown:

------------
``shutdown``
------------

Usage: ``denzel shutdown [OPTIONS]``

Stops and deletes all services, if you wish only to stop use the :ref:`stop` command.

.. option:: --purge|--no-purge

    Discard the docker images

    Default: ``--no-purge``

++++++++
Examples
++++++++

 - Shutdown a denzel project, removing all containers

    .. code-block:: bash

        $ denzel shutdown

 - Shutdown a denzel project, removing all containers and remove related docker images (denzel and redis)

    .. code-block:: bash

        $ denzel shutdown --purge

.. _start:

---------
``start``
---------

Usage: ``denzel start``

Start services

++++++++
Examples
++++++++

Start the application services

    .. code-block:: bash

        $ denzel start

.. _stop:

--------
``stop``
--------

Usage: ``denzel stop``

Stop services

++++++++
Examples
++++++++

Start the application services

    .. code-block:: bash

        $ denzel stop

.. _restart:

-----------
``restart``
-----------

Usage: ``denzel restart``

Restart services (equal to calling :ref:`stop` and then :ref:`start`).

++++++++
Examples
++++++++

Restart the denzel services

    .. code-block:: bash

        $ denzel restart

.. _status:

----------
``status``
----------

Usage: ``denzel status [OPTIONS]``

Examine status of services and worker. Use this to monitor the status of your project.

.. option:: --live|--no-live

    Live status view

    Default: ``--no-live``

++++++++
Examples
++++++++

 - Examine application status, statically

    .. code-block:: bash

        $ denzel status

 - View application status in a live manner, automatically updating

    .. code-block:: bash

        $ denzel status --live

.. _logs:

--------
``logs``
--------

Usage: ``denzel logs [OPTIONS]``

Show service logs

.. option:: --service [api|denzel|monitor|redis|all]

    Target service

    Default: ``all``

.. option:: --live|--no-live

    Follow logs output

    Default: ``--no-live``

++++++++
Examples
++++++++

 - Examine all of the services logs, statically

    .. code-block:: bash

        $ denzel logs

 - Examine only the ``denzel`` service logs, statically

    .. code-block:: bash

        $ denzel logs --service denzel

 - View all of the service logs in a live manner, automatically updating

    .. code-block:: bash

        $ denzel logs --live

.. _logworker:

-------------
``logworker``
-------------

Usage: ``denzel logworker [OPTIONS]``

Show worker log

.. option:: --live|--no-live

    Follow logs output

    Default: ``--no-live``

++++++++
Examples
++++++++

 - Examine the worker logs, statically

    .. code-block:: bash

        $ denzel logworker

 - View the worker logs in a live manner, automatically updating

    .. code-block:: bash

        $ denzel logs --service denzel

.. _shell:

---------
``shell``
---------

Usage: ``denzel shell [OPTIONS]``

Connect to service bash shell. This is only for advanced usage, shouldn't be used in standard scenarios.

.. option:: --service [api|denzel|monitor|redis]

    Target service

    Default: ``denzel``

++++++++
Examples
++++++++

 - Start an interactive shell session in the ``denzel`` service (default)

    .. code-block:: bash

        $ denzel shell

 - Start an interactive shell session in the ``api`` service

    .. code-block:: bash

        $ denzel shell --service api


.. _updateosreqs:

----------------
``updateosreqs``
----------------

Usage: ``denzel updateosreqs``

Run shell commands from ``requirements.sh``. This command uses ``/bin/bash`` for execution and treats the file as a bash script.
Notice, that due to docker and ``apt`` caching issues, if you have a ``apt-get install`` command, make sure you precede it with ``update``, e.g. ``apt-get update && apt-get install <package-name>``.
There is no need to use ``sudo``, these commands will run as root.

.. note::

    Every time you call ``updateosreqs``, all of the contents of ``requirements.sh`` will be executed.

++++++++
Examples
++++++++

Install ``htop`` command on all services

.. code-block:: bash

    $ echo "apt-get update && apt-get install htop" >> requirements.sh
    $ denzel updateosreqs


.. _updatepipreqs:

--------------
``updatepipreqs``
--------------

Usage: ``denzel updatepipreqs``

Update services according to ``requirements.txt``. This command always uses the pip ``--upgrade`` flag, so requirements will always be updated to the latest version.
If you wish to install a specific version, specify it in the ``requirements.txt`` file. This command will initiate a restart so updates will apply.

++++++++
Examples
++++++++

Update the Python packages using the ``requirements.txt`` file

    .. code-block:: bash

        $ denzel updatepipreqs

.. _updatereqs:

--------------
``updatereqs``
--------------

Usage: ``denzel updatereqs``

Updates services according to ``requirements.txt`` and ``requirements.sh``, equivalent to calling ``updatepipreqs`` and ``updateosreqs`` consecutively, but faster.

++++++++
Examples
++++++++

Update the Python packages using ``requirements.txt`` and execute shell script ``requirements.sh``

    .. code-block:: bash

        $ denzel updatereqs

.. _response:

------------
``response``
------------

Usage ``denzel response [OPTIONS]``

Set response manner (sync/async) and sync timeout

.. option:: --sync|--async

    Responses synchronicity  [required]

.. option:: --timeout

    Sync response timeout in seconds

    Default: ``5.0``

++++++++
Examples
++++++++

 - Set synchronous response mode (default)

    .. code-block:: bash

        $ denzel --sync

 - Set asynchronous response mode with the default response timeout of 5 seconds

    .. code-block:: bash

        $ denzel --async

 - Set asynchronous response mode with response timeout of 10 seconds

    .. code-block:: bash

        $ denzel --async --timeout 10
