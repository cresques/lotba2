
Hay problemas de carga de datos de los XML en las tablas porque hay campos que estan marcados como NOT NULL pero que no tienen valores.
Una estrategia de depuracion (Puede que los XML esten mal pero puede que las tablas sean demasiado estrictas) es eliminar los not null problematicos.

Dejo aqui la definicion original de las tablas, para poder restaurarla si es necesario.
```SQL
-- CREATE RUD_D Antes de quitar controles de NOT NULL
CREATE TABLE `RUD_D` (
  `Dia` date NOT NULL,
  `JugadorId` int(11) NOT NULL,
  `FechaActivacion` timestamp NOT NULL,
  `CambioDatos` varchar(1) NOT NULL,
  `Residente_Nacionalidad` varchar(2) DEFAULT NULL,
  `Residente_DNI` varchar(20) DEFAULT NULL,
  `NoResidente_Nacionalidad` varchar(2) DEFAULT NULL,
  `NoResidente_Documento` varchar(20) DEFAULT NULL,
  `NoResidente_PaisResidencia` varchar(2) DEFAULT NULL,
  `NoResidente_TipoDocumento` int(1) DEFAULT NULL,
  `NoResidente_EspecificarTipoDocumento` varchar(20) DEFAULT NULL,
  `FechaNacimiento` date NOT NULL,
  `Login` varchar(50) DEFAULT NULL,
  `Pseudonimo` varchar(100) DEFAULT NULL,
  `CUIT` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `Nombre` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Apellido` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Sexo` varchar(1) DEFAULT NULL,
  `EstadoCivil` varchar(40) DEFAULT NULL,
  `Domicilio_Direccion` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Domicilio_Ciudad` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Domicilio_Pais` varchar(2) NOT NULL,
  `Telefono` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Ocupacion` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Debería ser NOT NULL?',
  `PEP` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RePET` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `LimitesDepositoDiario` decimal(20,2) NOT NULL,
  `LimitesDepositoSemanal` decimal(20,2) NOT NULL,
  `LimitesDepositoMensual` decimal(20,2) NOT NULL,
  `LimitesGasto` decimal(20,2) NOT NULL DEFAULT '1500000.00',
  `LimitesTiempo` decimal(20,2) NOT NULL DEFAULT '6.00',
  `LimitesPerdida` decimal(20,2) NOT NULL DEFAULT '1500000.00',
  `VDocumental` varchar(1) NOT NULL,
  `FVDocumental` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`Dia`,`JugadorId`),
  KEY `idx_JugadorId` (`JugadorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `RUD_D_Estado` (
  `Dia` date NOT NULL,
  `JugadorId` int(11) NOT NULL,
  `Desde` timestamp NOT NULL,
  `EstadoCNJ` varchar(20) NOT NULL,
  `EstadoOperador` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Dia`,`JugadorId`,`Desde`,`EstadoCNJ`,`EstadoOperador`),
  KEY `idx_JugadorId` (`JugadorId`,`Dia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


Create Table

CREATE TABLE `RUD_M` (
  `Anno` int(4) NOT NULL,
  `Mes` int(2) NOT NULL,
  `JugadorId` int(11) NOT NULL,
  `FechaActivacion` timestamp NOT NULL,
  `CambioDatos` varchar(1) NOT NULL,
  `Residente_Nacionalidad` varchar(2) DEFAULT NULL,
  `Residente_DNI` varchar(20) DEFAULT NULL,
  `NoResidente_Nacionalidad` varchar(2) DEFAULT NULL,
  `NoResidente_Documento` varchar(20) DEFAULT NULL,
  `NoResidente_PaisResidencia` varchar(2) DEFAULT NULL,
  `NoResidente_TipoDocumento` int(1) DEFAULT NULL,
  `NoResidente_EspecificarTipoDocumento` varchar(20) DEFAULT NULL,
  `FechaNacimiento` date NOT NULL,
  `Login` varchar(50) DEFAULT NULL,
  `Pseudonimo` varchar(100) DEFAULT NULL,
  `CUIT` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `Nombre` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Apellido` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Sexo` varchar(1) DEFAULT NULL,
  `EstadoCivil` varchar(40) DEFAULT NULL,
  `Domicilio_Direccion` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Domicilio_Ciudad` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Domicilio_Pais` varchar(2) NOT NULL,
  `Telefono` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Ocupacion` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Debería ser NOT NULL?',
  `PEP` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RePET` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `LimitesDepositoDiario` decimal(20,2) NOT NULL,
  `LimitesDepositoSemanal` decimal(20,2) NOT NULL,
  `LimitesDepositoMensual` decimal(20,2) NOT NULL,
  `LimitesGasto` decimal(20,2) NOT NULL DEFAULT '1500000.00',
  `LimitesTiempo` decimal(20,2) NOT NULL DEFAULT '6.00',
  `LimitesPerdida` decimal(20,2) NOT NULL DEFAULT '1500000.00',
  `VDocumental` varchar(1) NOT NULL,
  `FVDocumental` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`Anno`,`Mes`,`JugadorId`),
  KEY `JugadorId` (`JugadorId`,`Anno`,`Mes`),
  KEY `Mes` (`Mes`,`Anno`,`JugadorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `RUD_M_Estado` (
  `Anno` int(4) NOT NULL,
  `Mes` int(2) NOT NULL,
  `JugadorId` int(11) NOT NULL,
  `Desde` timestamp NOT NULL,
  `EstadoCNJ` varchar(20) NOT NULL,
  `EstadoOperador` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`Anno`,`Mes`,`JugadorId`,`Desde`,`EstadoCNJ`),
  KEY `JugadorId` (`JugadorId`,`Anno`,`Mes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

```
