Atlast package
^^^^^^^^^^^^^^

.. uml::

    @startuml atlast_sc_pacakge

    left to right direction

    package "calculator" as atlast_sc.calculator {
    }
    package "data" as atlast_sc.data {
    }
    package "derived_groups" as atlast_sc.derived_groups {
    }
    package "exceptions" as atlast_sc.exceptions {
    }
    package "models" as atlast_sc.models {
    }
    package "utils" as atlast_sc.utils {
    }
    atlast_sc.calculator --> atlast_sc.derived_groups
    atlast_sc.calculator --> atlast_sc.exceptions
    atlast_sc.calculator --> atlast_sc.models
    atlast_sc.calculator --> atlast_sc.utils
    atlast_sc.data --> atlast_sc.exceptions
    atlast_sc.data --> atlast_sc.utils
    atlast_sc.models --> atlast_sc.data
    atlast_sc.models --> atlast_sc.exceptions
    @enduml