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
      pinstall      Install pip packages to running services
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

-----------------
``startproject``
-----------------

Usage: ``denzel startproject NAME``

Builds the denzel project skeleton

.. py:attribute:: NAME

    Name of the project

.. option:: --gpu|--no-gpu

    Support for NVIDIA GPU

    Default: ``--no-gpu``


.. _launch:

----------
``launch``
----------

Usage: ``denzel launch [OPTIONS]``

Builds and starts all services

.. option:: --api-monitor <INTEGER>

    API endpoints port

    Default: ``8000``

.. option:: --monitor-monitor <INTEGER>

    Monitor UI port

    Default: ``5555``


.. _shutdown:

------------
``shutdown``
------------

Usage: ``denzel shutdown [OPTIONS]``

Stops and deletes all services

.. option:: --purge|--no-purge

    Discard the docker images

    Default: ``--no-purge``


.. _start:

---------
``start``
---------

Usage: ``denzel start``

Start services


.. _stop:

--------
``stop``
--------

Usage: ``denzel stop``

Stop services


.. _restart:

-----------
``restart``
-----------

Usage: ``denzel restart``

Restart services


.. _status:

----------
``status``
----------

Usage: ``denzel status``

Examine status of services


.. _pinstall:

------------
``pinstall``
------------

Usage: ``denzel pinstall [OPTIONS] [PACKAGES]``

Install pip packages to running services

.. option:: --service [api|denzel|monitor]

    Target service

    Default: ``denzel``

.. option:: --upgrade|--no-upgrade

    Upgrade if already installed

    Default: ``--no-upgrade``

.. option:: --req-append|--no-req-append

    Append to requirements.txt file

    Default: ``--req-append``

.. py:attribute:: PACKAGES

    Space separated pip packages


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



.. _logworker:

-------------
``logworker``
-------------

Usage: ``denzel logworker [OPTIONS]``

Show worker log

.. option:: --live|--no-live

    Follow logs output

    Default: ``--no-live``


.. _shell:

---------
``shell``
---------

Usage: ``denzel shell [OPTIONS]``

Connect to service bash shell

.. option:: --service [api|denzel|monitor|redis]

    Target service

    Default: ``denzel``


.. _updatereqs:

--------------
``updatereqs``
--------------

Usage: ``denzel updatereqs [OPTIONS]``

Update service according to requirements.txt

.. option:: --service [api|denzel|monitor]

    Target service

    Default: ``denzel``

.. option:: --upgrade|--no-upgrade

    Upgrade if already installed

    Default: ``--no-upgrade``