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
      launch        Builds and starts all services
      logs          Show service logs
      logworker     Show worker log
      restart       Restart services
      shell         Connect to service bash shell
      shutdown      Stops and deletes all services
      start         Start services
      startproject  Builds the denzel project skeleton
      status        Examine status of services
      stop          Stop services
      updatereqs    Update service according to requirements.txt


| For command specific help you can follow a command with the ``--help`` flag (ex. ``denzel launch --help``)


.. contents:: Commands
    :local:

.. note::
    Except from the :ref:`startproject` command, all other commands must be executed from within project directory


.. _startproject:

------------
startproject
------------

Usage: ``denzel startproject NAME``

Builds the denzel project skeleton.

.. py:attribute:: NAME

    Name of the project

.. option:: --gpu|--no-gpu

    Support for NVIDIA GPU

    Default: ``--no-gpu``


.. _launch:

------
launch
------

Usage: ``denzel launch [OPTIONS]``

Builds and starts all services.

.. option:: --api-port <INTEGER>

    API endpoints port

    Default: ``8000``

.. option:: --monitor-port <INTEGER>

    Monitor UI port

    Default: ``5555``


.. _shutdown:

--------
shutdown
--------

Usage: ``denzel shutdown [OPTIONS]``

Stops and deletes all services, if you wish only to stop use the :ref:`stop` command.

.. option:: --purge|--no-purge

    Discard the docker images

    Default: ``--no-purge``


.. _start:

-----
start
-----

Usage: ``denzel start``

Start services


.. _stop:

----
stop
----

Usage: ``denzel stop``

Stop services


.. _restart:

-------
restart
-------

Usage: ``denzel restart``

Restart services (equal to calling :ref:`stop` and then :ref:`start`).


.. _status:

------
status
------

Usage: ``denzel status [OPTIONS]``

Examine status of services and worker. Use this to monitor the status of your project.

.. option:: --live|--no-live

    Live status view

    Default: ``--no-live``

.. _logs:

----
logs
----

Usage: ``denzel logs [OPTIONS]``

Show service logs

.. option:: --service [api|denzel|monitor|redis|all]

    Target service

    Default: ``all``

.. option:: --live|--no-live

    Follow logs output

    Default: ``--no-live``



.. _logworker:

---------
logworker
---------

Usage: ``denzel logworker [OPTIONS]``

Show worker log

.. option:: --live|--no-live

    Follow logs output

    Default: ``--no-live``


.. _shell:

-----
shell
-----

Usage: ``denzel shell [OPTIONS]``

Connect to service bash shell. This is only for advanced usage, shouldn't be used in standard scenarios.

.. option:: --service [api|denzel|monitor|redis]

    Target service

    Default: ``denzel``


.. _updatereqs:

----------
updatereqs
----------

Usage: ``denzel updatereqs``

Update services according to ``requirements.txt``. This command always uses the pip ``--upgrade`` flag, so requirements will always be updated to the latest version.
If you wish to install a specific version, specify it in the ``requirements.txt`` file. This command will initiate a restart so updates will apply.

