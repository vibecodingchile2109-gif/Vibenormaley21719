---
tipo: documento interno / doctrina propia (NO normativo)
autor: Matías Rojas Faúndez — VibeCodingChile
fecha: Julio 2026, v1.0.0
advertencia: "Contiene numeración de artículos propia del autor que NO coincide con el articulado oficial. No usar como fuente de citas legales."
uso: Explicar la arquitectura de Gobernador IA y su mapeo a controles
---

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Gobernador IA y la Ley 21.719: Arquitectura
     Técnica como Instrumento de Gobernanza de
     Datos Personales en Chile
     Análisis técnico-jurídico comparado con ISO/IEC 42001:2023, EU AI Act y marcos de
     responsabilidad para agentes de IA autónomos

     Autor: Matías Germán Valentín Rojas Faúndez
     Licenciado en Ciencias Jurídicas, UCINF
     Founder, VibeCodingChile | Dense y Sparse | Legalizespa
     Fecha: Julio 2026
     Versión: 1.0.0
     Clasificación: Análisis técnico-jurídico — Uso externo

     Resumen Ejecutivo
     El presente paper establece la correspondencia técnico-jurídica entre la arquitectura de tres capas
     del sistema Gobernador IA (/Python, CheckWizard/Rust, React) y los estándares de cumplimiento
     exigidos por la Ley 21.719 (Ley de Protección de Datos Personales de Chile, en vigencia), la
     ISO/IEC 42001:2023 (Sistema de Gestión de IA) y el EU AI Act como marco comparado de
     referencia obligatoria para operaciones transfronterizas.

     La tesis central es que el cumplimiento normativo no es un artefacto jurídico superpuesto al
     desarrollo, sino una propiedad emergente de la arquitectura. Cada decisión de diseño en
     Gobernador IA —desde el modelo de aislamiento de subagentes hasta el sistema de trazabilidad
     inmutable vía CheckWizard— puede expresarse como una implementación directa de un artículo
     de la Ley 21.719, un control ISO/IEC 42001:2023 o una obligación del EU AI Act.

     Complementariamente, el paper integra los hallazgos del Discussion Paper "Legal Responsibility
     for AI Agents" (IMDA, mayo 2026) y los marcos pedagógicos del "Responsible AI Use Planning
     Guide" (Pavuluri, 2026) para construir un análisis de responsabilidad civil aplicable al despliegue de
     agentes autónomos en el contexto chileno, donde la cadena de valor incluye desarrollador de
     modelo, proveedor de herramientas, desplegador empresarial y usuario final.

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Tabla de Contenidos
          1. Contexto Normativo: La Ley 21.719 como Mandato Técnico
          2. Arquitectura de Gobernador IA: Descripción Técnica por Capa
          3. Mapeo Capa-a-Artículo: Ley 21.719 vs. Implementación
          4. ISO/IEC 42001:2023: Controles Mapeados a Componentes del Sistema
          5. EU AI Act: Marco Comparado para Operaciones Transfronterizas
          6. Responsabilidad Legal de Agentes IA: Integración del Marco IMDA 2026
          7. Análisis de la Cadena de Responsabilidad en el Contexto Chileno
          8. Anonymization como Control Técnico y Obligación Normativa
          9. Responsible AI Use Planning: Marco Pedagógico Integrado
        10. Arquitectura de Evidencia: Trazabilidad Inmutable como Prueba Legal
        11. Modelo de Riesgo Diferenciado por Actor en la Cadena de Valor
        12. NORMA: Agente Conversacional como Interfaz de Gobernanza
        13. Conclusiones y Líneas de Desarrollo
        14. Referencias Normativas y Técnicas

     1. Contexto Normativo: La Ley 21.719 como Mandato
     Técnico

     La Ley 21.719, promulgada el 13 de diciembre de 2024 y publicada el 13 de enero de 2025,
     establece el nuevo marco de protección de datos personales en Chile, derogando parcialmente la
     Ley 19.628. Su entrada en vigencia plena opera en fases, con el régimen sancionatorio activándose
     en diciembre de 2026. Este horizonte temporal define exactamente la ventana de mercado que
     Gobernador IA ocupa.

     La arquitectura normativa de la Ley 21.719 descansa sobre cinco pilares técnicamente
     operacionalizables:

     Pilar I — Bases de licitud del tratamiento (Arts. 12-16): El tratamiento de datos personales
     requiere una base jurídica explícita: consentimiento, ejecución de contrato, interés legítimo,
     obligación legal, o interés vital. Cada operación de tratamiento ejecutada por un agente de IA debe
     poder ser rastreada a una de estas bases en tiempo real.

     Pilar II — Derechos del titular (Arts. 4-11, 54-57): Los derechos ARCO ampliados (Acceso,
     Rectificación, Cancelación/Eliminación, Oposición, Portabilidad, y en el caso chileno el derecho a no
     ser objeto de decisiones automatizadas) imponen obligaciones de respuesta en plazos definidos. El

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Art. 54 de la Ley 19.628, actualizado, y el Art. 55 del nuevo marco establecen el derecho a no ser
     objeto de decisiones automatizadas que produzcan efectos jurídicos significativos sin intervención
     humana verificable.

     Pilar III — Responsabilidad proactiva (Art. 14, principio de accountability): El responsable del
     tratamiento debe poder demostrar —no solo declarar— el cumplimiento. Este principio transforma
     el compliance de un acto declarativo en un sistema de evidencia continua.

     Pilar IV — Evaluación de impacto (Arts. 15 bis y siguientes): Las operaciones de alto riesgo,
     incluyendo el uso de IA para decisiones automatizadas sobre personas, requieren una Evaluación
     de Impacto en Protección de Datos (EIPD) previa. Esto mapea directamente al concepto de DPIA
     en GDPR y al requisito de evaluación de riesgo en ISO/IEC 42001:2023, Sección 6.1.

     Pilar V — Régimen sancionatorio escalonado: Las multas alcanzan hasta 5.000 UTM para
     infracciones graves, con la Agencia de Protección de Datos Personales (APDP) como órgano
     fiscalizador. La Ley 21.663 de Ciberseguridad complementa este régimen para incidentes de
     seguridad.

     La tesis arquitectónica de Gobernador IA es que cada uno de estos cinco pilares puede ser
     implementado como un control técnico verificable dentro de la stack Python/Rust/React,
     eliminando la brecha entre declaración normativa y evidencia operacional.

     2. Arquitectura de Gobernador IA: Descripción Técnica por
     Capa

     Gobernador IA opera sobre una arquitectura de tres capas con responsabilidades funcionales
     diferenciadas:

     Capa 1: OpenFang / Python — Orquestación de Agentes

        # Ejemplo: Motor de consentimiento con base jurídica explícita
        # Gobernador IA / OpenFang Layer - consent_engine.py

        from dataclasses import dataclass, field
        from datetime import datetime
        from enum import Enum
        from typing import Optional
        import hashlib
        import json
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

        class BaseLicitud(Enum):
                """
                Art. 12 Ley 21.719: Bases de licitud del tratamiento
                """
                CONSENTIMIENTO = "consentimiento"                                   # Art. 12 a)
                EJECUCION_CONTRATO = "ejecucion_contrato"                           # Art. 12 b)
                OBLIGACION_LEGAL = "obligacion_legal"                               # Art. 12 c)
                INTERES_VITAL = "interes_vital"                                     # Art. 12 d)
                INTERES_LEGITIMO = "interes_legitimo"                               # Art. 12 e)
                INTERES_PUBLICO = "interes_publico"                                 # Art. 12 f)

        @dataclass
        class RegistroTratamiento:
                """
                Art. 14 Ley 21.719: Registro de actividades de tratamiento
                ISO/IEC 42001:2023 Sección 8.4: Gestión de datos
                """
                id_operacion: str
                titular_hash: str                         # Pseudonimización obligatoria
                finalidad: str
                base_licitud: BaseLicitud
                datos_categorias: list[str]
                timestamp_inicio: datetime
                responsable_tratamiento: str
                sub_encargados: list[str] = field(default_factory=list)
                timestamp_fin: Optional[datetime] = None
                revocado: bool = False

                def to_audit_record(self) -> dict:
                      """Genera registro inmutable para CheckWizard/Rust"""
                      record = {
                           "id": self.id_operacion,
                           "titular_hash": self.titular_hash,
                           "base_licitud": self.base_licitud.value,
                           "finalidad": self.finalidad,
                           "timestamp": self.timestamp_inicio.isoformat(),
                           "responsable": self.responsable_tratamiento,
                      }
                      # Fingerprint criptográfico para integridad
                      record["integrity_hash"] = hashlib.sha256(

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                            json.dumps(record, sort_keys=True).encode()
                      ).hexdigest()
                      return record

        class ConsentEngine:
                """
                Motor de gestión de consentimiento con base jurídica explícita.
                Cumplimiento: Art. 12-14 Ley 21.719
                ISO/IEC 42001:2023: Sección 6.1.2 - Evaluación de riesgos de IA
                """

                def __init__(self, audit_bus):
                      self.audit_bus = audit_bus
                      self._registros: dict[str, RegistroTratamiento] = {}

                def iniciar_tratamiento(
                      self,
                      titular_rut: str,
                      finalidad: str,
                      base_licitud: BaseLicitud,
                      datos: list[str],
                      responsable: str,
                ) -> RegistroTratamiento:
                      """
                      Registra operación de tratamiento con base jurídica verificable.
                      Toda operación de agente que involucre datos personales DEBE
                      pasar por este método antes de ejecutarse.
                      """
                      titular_hash = hashlib.sha256(titular_rut.encode()).hexdigest()

                      registro = RegistroTratamiento(
                            id_operacion=f"OP-{datetime.utcnow().timestamp()}",
                            titular_hash=titular_hash,
                            finalidad=finalidad,
                            base_licitud=base_licitud,
                            datos_categorias=datos,
                            timestamp_inicio=datetime.utcnow(),
                            responsable_tratamiento=responsable,
                      )

                      self._registros[registro.id_operacion] = registro

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                    # Envío inmediato a capa de auditoría Rust
                    self.audit_bus.emit(registro.to_audit_record())
                    return registro

                def ejercer_derecho_arco(
                    self,
                    titular_rut: str,
                    derecho: str
                ) -> dict:
                    """
                    Art. 11 Ley 21.719: Plazos de respuesta a derechos ARCO.
                    Máximo 15 días hábiles para acceso, 5 para supresión urgente.
                    """
                    titular_hash = hashlib.sha256(titular_rut.encode()).hexdigest()
                    registros_titular = [
                           r for r in self._registros.values()
                           if r.titular_hash == titular_hash and not r.revocado
                    ]
                    return {
                           "titular": titular_hash,
                           "derecho_solicitado": derecho,
                           "operaciones_activas": len(registros_titular),
                           "plazo_respuesta_dias": 15,
                           "timestamp_solicitud": datetime.utcnow().isoformat(),
                    }

     Capa 2: CheckWizard / Rust — Verificación y Trazabilidad Inmutable

        // CheckWizard - audit_ledger.rs
        // Capa de trazabilidad inmutable: Art. 14 Ley 21.719 + ISO/IEC 42001:2023 Sección 9.

        use sha2::{Digest, Sha256};
        use std::collections::HashMap;
        use chrono::{DateTime, Utc};
        use serde::{Deserialize, Serialize};

        /// Registro de auditoría inmutable por operación de tratamiento
        /// Implementa: Art. 14 Ley 21.719 (principio accountability)
        /// ISO/IEC 42001:2023 Sección 9.1.3: Evidencia de conformidad
        #[derive(Debug, Clone, Serialize, Deserialize)]

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

        pub struct AuditRecord {
                pub id: String,
                pub titular_hash: String,
                pub base_licitud: String,
                pub finalidad: String,
                pub timestamp: DateTime<Utc>,
                pub responsable: String,
                pub integrity_hash: String,
                pub chain_hash: Option<String>,                      // Enlace al registro anterior (blockchain-styl
        }

        /// Verificador de conformidad normativa por artículo
        /// Cada regla mapea directamente a un artículo de la Ley 21.719
        #[derive(Debug)]
        pub struct ComplianceRule {
                pub articulo: String,                        // e.g., "Art. 12 Ley 21.719"
                pub descripcion: String,
                pub validator: Box<dyn Fn(&AuditRecord) -> Result<(), String> + Send + Sync>,
        }

        pub struct CheckWizard {
                ledger: Vec<AuditRecord>,
                rules: Vec<ComplianceRule>,
                violations: Vec<(String, String, String)>, // (record_id, articulo, mensaje)
        }

        impl CheckWizard {
                pub fn new() -> Self {
                    let mut wizard = CheckWizard {
                           ledger: Vec::new(),
                           rules: Vec::new(),
                           violations: Vec::new(),
                    };
                    wizard.register_ley21719_rules();
                    wizard
                }

                /// Registra reglas de cumplimiento mapeadas a artículos Ley 21.719
                fn register_ley21719_rules(&mut self) {
                    // Art. 12: Base de licitud requerida
                    self.rules.push(ComplianceRule {

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                           articulo: "Art. 12 Ley 21.719".to_string(),
                           descripcion: "Todo tratamiento debe tener base de licitud explícita".to_s
                           validator: Box::new(|record| {
                                 if record.base_licitud.is_empty() {
                                        Err("Base de licitud no declarada — violación Art. 12".to_string(
                                 } else {
                                        Ok(())
                                 }
                           }),
                    });

                    // Art. 14: Registro de actividades verificable
                    self.rules.push(ComplianceRule {
                           articulo: "Art. 14 Ley 21.719".to_string(),
                           descripcion: "Registro de actividades debe ser íntegro y verificable".to_
                           validator: Box::new(|record| {
                                 let expected_hash = Self::compute_hash(record);
                                 if record.integrity_hash != expected_hash {
                                        Err("Integridad del registro comprometida — violación Art. 14".to
                                 } else {
                                        Ok(())
                                 }
                           }),
                    });

                    // Art. 54-55 (Ley 19.628 actualizada): Decisiones automatizadas
                    self.rules.push(ComplianceRule {
                           articulo: "Art. 55 Ley 19.628 / Art. 21 EU AI Act (ref. comparado)".to_st
                           descripcion: "Decisiones con efectos jurídicos sobre persona natural requ
                           validator: Box::new(|record| {
                                 if record.finalidad.contains("decision_automatizada")
                                        && !record.finalidad.contains("hitl_verificado") {
                                        Err("Decisión automatizada sin HITL documentado".to_string())
                                 } else {
                                        Ok(())
                                 }
                           }),
                    });
                }

                fn compute_hash(record: &AuditRecord) -> String {

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                    let content = format!("{}{}{}{}",
                           record.id, record.titular_hash, record.base_licitud, record.timestamp);
                    format!("{:x}", Sha256::digest(content.as_bytes()))
                }

                /// Ingesta registro desde capa Python y ejecuta todas las reglas
                pub fn ingest_and_verify(&mut self, record: AuditRecord) -> Vec<String> {
                    let mut failures = Vec::new();

                    for rule in &self.rules {
                           if let Err(msg) = (rule.validator)(&record) {
                                 failures.push(format!("[{}] {}", rule.articulo, msg));
                                 self.violations.push((
                                        record.id.clone(),
                                        rule.articulo.clone(),
                                        msg
                                 ));
                           }
                    }

                    // Cadena de hashes para inmutabilidad (blockchain-style)
                    let chain_hash = self.ledger.last()
                           .map(|prev| prev.integrity_hash.clone());

                    let mut stored = record;
                    stored.chain_hash = chain_hash;
                    self.ledger.push(stored);

                    failures
                }

                /// Genera reporte de cumplimiento por artículo
                pub fn compliance_report(&self) -> HashMap<String, usize> {
                    let mut violations_by_article: HashMap<String, usize> = HashMap::new();
                    for (_, articulo, _) in &self.violations {
                           *violations_by_article.entry(articulo.clone()).or_insert(0) += 1;
                    }
                    violations_by_article
                }
        }

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Capa 3: React — Dashboard de Gobernanza y Visualización de Cumplimiento

     La capa React actúa como interfaz de control para el Delegado de Protección de Datos (DPO), el
     responsable de seguridad y la dirección ejecutiva. Expone en tiempo real el estado de
     cumplimiento por artículo de la Ley 21.719, el mapa de calor de riesgos ISO/IEC 42001:2023, y los
     registros de violaciones detectadas por CheckWizard.

     3. Mapeo Capa-a-Artículo: Ley 21.719 vs. Implementación

       Artículo
          Ley           Obligación                      Componente Gobernador IA                          Implementación
        21.719

                      Base de licitud
                                                                                                      Enum BaseLicitud con
       Art. 12        del                       ConsentEngine.iniciar_tratamiento()
                                                                                                      6 bases jurídicas
                      tratamiento

                      Derechos
                                                                                                      Timestamp + SLA
       Art. 11        ARCO — plazo              ConsentEngine.ejercer_derecho_arco()
                                                                                                      automático
                      15 días

                      Registro de
                                                                                                      Serialización + hash
       Art. 14        actividades de            RegistroTratamiento.to_audit_record()
                                                                                                      SHA-256
                      tratamiento

       Art. 14        Principio de                                                                    Verificación automática
                                                CheckWizard.ingest_and_verify()
       bis            accountability                                                                  por regla-artículo

                      Evaluación de                                                                   Scoring automático de
       Art. 15                                 Pipeline EIPD en OpenFang
                      impacto (EIPD)                                                                  riesgo por operación

       Art. 54-                                                                                       Detección de
                      Decisiones
       55 (Ley                                 Regla Art. 55 en CheckWizard                           decision_automatizada
                      automatizadas
       19.628)                                                                                        sin HITL

                                                                                                      Lista de terceros
                      Transferencias
       Art. 28                                  sub_encargados en RegistroTratamiento                 procesadores por
                      internacionales
                                                                                                      operación

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

       Artículo
          Ley           Obligación                      Componente Gobernador IA                         Implementación
        21.719

                      Medidas de                                                                      Hash de cadena
       Art. 32                                 Capa Rust con verificación de integridad
                      seguridad                                                                       blockchain-style

     4. ISO/IEC 42001:2023: Controles Mapeados a Componentes
     del Sistema
     La ISO/IEC 42001:2023 es el primer estándar internacional de sistema de gestión para IA. Su
     estructura sigue el High Level Structure (HLS) de las normas ISO de gestión, lo que permite
     integración directa con ISO 27001 (seguridad de la información) e ISO 9001 (calidad).

     Los controles del Anexo A de la ISO/IEC 42001:2023 se mapean a Gobernador IA de la siguiente
     manera:

     Control A.2.2 — Política de IA: Gobernador IA genera automáticamente un borrador de política
     de IA basado en el catálogo de operaciones de tratamiento activas. NORMA actúa como agente
     conversacional para interpretar la política ante auditores.

     Control A.3.2 — Roles y responsabilidades: El sistema registra el responsable_tratamiento y
      sub_encargados por cada operación, creando un mapa de roles verificable en tiempo real.

     Control A.6.1 — Evaluación de riesgos del sistema de IA: El pipeline de EIPD en OpenFang
     ejecuta una evaluación de riesgo automática antes de cada despliegue de agente nuevo, scoring
     según matriz probabilidad × impacto.

     Control A.6.2 — Tratamiento de riesgos: Las violaciones detectadas por CheckWizard disparan
     automáticamente un flujo de tratamiento de riesgo con opciones predefinidas: mitigar, aceptar,
     transferir, evitar.

     Control A.8.4 — Gestión de datos para sistemas de IA: El módulo de pseudonimización en
     OpenFang (hash SHA-256 del RUT) implementa este control directamente. Los datos categorizados
     en RegistroTratamiento.datos_categorias alimentan el inventario de datos del sistema de
     gestión.
                                                                                                                         

     Control A.9.1 — Monitoreo, medición, análisis y evaluación: CheckWizard genera métricas de
     cumplimiento por artículo disponibles vía API para el dashboard React. El compliance_report() es
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     el artefacto de evidencia para auditorías internas.

     Control A.10.1 — No conformidades y acciones correctivas: Cada entrada en
      CheckWizard.violations constituye una no conformidad registrada con trazabilidad completa. El
     sistema genera automáticamente un plan de acción correctiva.

     5. EU AI Act: Marco Comparado para Operaciones
     Transfronterizas
     El EU AI Act (Reglamento UE 2024/1689, vigente desde agosto 2024 con fases de aplicación hasta
     2027) es el marco de referencia obligatorio para cualquier empresa chilena que procese datos de
     residentes europeos o que aspire a operar en mercados europeos.

     La relevancia directa para Gobernador IA es triple:

     Clasificación de riesgo (Arts. 6-9 EU AI Act): Los sistemas de IA que realizan decisiones
     automatizadas con efectos jurídicos sobre personas físicas en dominios como empleo, crédito, o
     servicios esenciales se clasifican como alto riesgo. NORMA, como agente conversacional de
     compliance legal, debe documentar explícitamente que sus outputs son asistencia a decisión
     humana, no decisiones autónomas, para evitar clasificación en Anexo III EU AI Act.

        # Ejemplo: Clasificador de riesgo EU AI Act integrado en NORMA
        class EUAIActRiskClassifier:
                """
                Arts. 6-9 EU AI Act: Clasificación de riesgo para sistemas de IA.
                Integrado en NORMA para auto-clasificación antes de despliegue.
                """
                HIGH_RISK_DOMAINS = [
                      "credito", "empleo", "educacion", "servicios_esenciales",
                      "administracion_justicia", "seguridad_publica"
                ]

                PROHIBITED_PRACTICES = [
                      "scoring_social", "manipulacion_subliminal",
                      "biometria_masa_espacio_publico"
                ]

                def classify(self, agent_description: str, output_type: str) -> dict:
                      """

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                    Clasifica el nivel de riesgo y genera requerimientos técnicos.
                    Art. 9 EU AI Act: Sistema de gestión de riesgo.
                    """
                    domain = self._detect_domain(agent_description)
                    is_autonomous_decision = output_type == "decision_vinculante"

                    if any(p in agent_description for p in self.PROHIBITED_PRACTICES):
                           return {"nivel": "PROHIBIDO", "articulo": "Art. 5 EU AI Act"}

                    if domain in self.HIGH_RISK_DOMAINS and is_autonomous_decision:
                           return {
                                 "nivel": "ALTO_RIESGO",
                                 "articulo": "Art. 6 + Anexo III EU AI Act",
                                 "requerimientos": [
                                        "Sistema de gestión de riesgo (Art. 9)",
                                        "Gobierno de datos (Art. 10)",
                                        "Documentación técnica (Art. 11)",
                                        "Registro de logs (Art. 12)",
                                        "Transparencia y usuarios (Art. 13)",
                                        "Supervisión humana (Art. 14)",
                                        "Exactitud, robustez y ciberseguridad (Art. 15)"
                                 ],
                                 "chile_mapping": "Ley 21.719 Art. 15 + ISO/IEC 42001:2023 Sección 6.1
                           }

                    return {
                           "nivel": "RIESGO_LIMITADO",
                           "articulo": "Art. 50 EU AI Act",
                           "requerimientos": ["Transparencia ante usuario"]
                    }

                def _detect_domain(self, description: str) -> str:
                    for domain in self.HIGH_RISK_DOMAINS:
                           if domain in description.lower():
                                 return domain
                    return "general"

     Responsabilidad en la cadena de valor (Arts. 16-27 EU AI Act): El Reglamento distingue entre
     providers (desarrolladores del modelo base) y deployers (quienes despliegan el sistema). Esta
     distinción es directamente analógica a la cadena de responsabilidad analizada por IMDA (2026) y

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     tiene implicancias concretas para VibeCodingChile en su rol simultáneo de developer (Gobernador
     IA) y deployer (clientes enterprise).

     Registro en la base de datos EU (Art. 71): Los sistemas de IA de alto riesgo deberán registrarse
     en la base de datos EU-OASIS antes de ser puestos en servicio en la UE. Gobernador IA implementa
     la generación automática del fichero de registro requerido.

     6. Responsabilidad Legal de Agentes IA: Integración del
     Marco IMDA 2026

     El Discussion Paper "Legal Responsibility for AI Agents" (IMDA, mayo 2026) es el análisis de
     responsabilidad civil más avanzado disponible para sistemas agénticos. Sus hallazgos son
     directamente aplicables al contexto chileno, con las adaptaciones que impone el sistema de
     derecho continental.

     El paper IMDA identifica tres desafíos centrales en la asignación de responsabilidad para agentes
     de IA:

     Desafío 1 — Autonomía y difusión de accountability: Los agentes que operan con autonomía
     reducida hacen difusa la cadena causal entre instrucción humana y resultado dañoso. En el
     contexto chileno, el Art. 2.309 del Código Civil (responsabilidad extracontractual por hecho
     propio) debe interpretarse a la luz del principio de accountability de la Ley 21.719: el responsable
     del tratamiento es responsable por las acciones del sistema que desplegó, independientemente del
     grado de autonomía de ese sistema.

     Desafío 2 — Multiplicidad de actores en la cadena de valor: El paper IMDA distingue: model
     developer → tooling provider → platform provider → system provider → deployer → end user →
     third parties. Para Gobernador IA, esta cadena se concreta así:

                                  Equivalente Gobernador
         Actor IMDA                                                                      Responsabilidad Ley 21.719
                                                   IA

       Model                                                                Responsabilidad por capacidades base del
                                 Anthropic (Claude API)
       developer                                                            modelo

                                                                            Responsabilidad por herramientas de
       Tooling provider          OpenFang SDK
                                                                            orquestación

                                                                            Responsabilidad por arquitectura y
       System provider           VibeCodingChile
                                                                            configuración
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                                  Equivalente Gobernador
         Actor IMDA                                                                      Responsabilidad Ley 21.719
                                                   IA

                                                                            Responsabilidad por despliegue y uso
       Deployer                  Cliente enterprise
                                                                            específico

       End user                  Empleados del cliente                      Responsabilidad por instrucciones y supervisión

       Third parties             Titulares de datos                         Derechos ARCO exigibles vía APDP

     Desafío 3 — Imprevisibilidad de comportamiento agéntico: El paper IMDA señala que incluso
     cuando todos los actores tomaron salvaguardas adecuadas, el agente puede comportarse de forma
     imprevisible causando daño. En el caso de la Ley 21.719, el Art. 14 bis (principio de
     accountability) y el Art. 32 (medidas de seguridad adecuadas) imponen al responsable del
     tratamiento la obligación de poder demostrar que adoptó medidas técnicas y organizativas
     apropiadas, independientemente del resultado.

     Gobernador IA implementa este estándar a través de la evidencia pre-generada: cada operación
     de tratamiento genera, antes de ejecutarse, un registro de las salvaguardas activas en ese
     momento. Si el agente produce un resultado dañoso, el responsable puede demostrar qué
     controles estaban activos, cuáles fueron sus outputs, y en qué punto se produjo la desviación.

     7. Análisis de la Cadena de Responsabilidad en el Contexto
     Chileno
     El derecho chileno no cuenta aún con jurisprudencia específica sobre responsabilidad de agentes
     de IA. Sin embargo, los principios generales de responsabilidad extracontractual del Código Civil
     (Arts. 2.314 y siguientes) y las disposiciones de la Ley 21.719 permiten construir un marco de
     análisis operacional.

     Análogo al caso Quoine v B2C2 (Singapur, 2020): El paper IMDA analiza este caso como
     precedente en el que contratos formados por algoritmos de trading fueron considerados
     vinculantes a pesar de una falla técnica. En Chile, la analogía aplica a decisiones de agentes IA en
     procesos de onboarding de clientes, scoring crediticio automatizado, o generación automática de
     documentos legales. La pregunta relevante —¿se atiende al estado mental del programador en el
     momento de escribir el código, o al resultado desde la perspectiva de un tercero razonable?— no
     tiene respuesta normativa clara en el derecho chileno actual. Gobernador IA adopta la posición más
     conservadora: toda decisión con efectos jurídicos requiere HITL (Human-in-the-Loop)
     verificable y registrado.
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Responsabilidad del deployer empresarial: Bajo la Ley 21.719, la empresa que despliega
     Gobernador IA para sus procesos internos es el responsable del tratamiento. VibeCodingChile
     actúa como encargado del tratamiento (Art. 2 letra m) Ley 21.719), lo que impone la obligación
     de suscribir un Contrato de Encargado de Tratamiento (DPA) con cláusulas técnicas específicas.
     Gobernador IA genera este contrato automáticamente con las especificaciones de cada
     deployment.

        # Generador automático de DPA — Gobernador IA / OpenFang
        class DPAGenerator:
                """
                Genera Contrato de Encargado de Tratamiento conforme Art. 2 letra m)
                y Art. 14 quáter Ley 21.719.
                """
                CLAUSULAS_OBLIGATORIAS_LEY21719 = [
                      "finalidad_unica_tratamiento",
                      "instrucciones_escritas_responsable",
                      "confidencialidad_personal_autorizado",
                      "medidas_seguridad_art32",
                      "subcontratacion_autorizada_responsable",
                      "asistencia_derechos_arco",
                      "devolucion_destruccion_datos_termino",
                      "auditoria_y_colaboracion",
                      "notificacion_violaciones_seguridad_72h",
                ]

                def generate(self, deployment_config: dict) -> dict:
                      dpa = {
                           "partes": {
                                 "responsable": deployment_config["cliente"],
                                 "encargado": "VibeCodingChile SpA",
                           },
                           "objeto": "Tratamiento de datos personales mediante sistema Gobernador IA
                           "base_legal": "Art. 14 quáter Ley 21.719",
                           "clausulas": {c: True for c in self.CLAUSULAS_OBLIGATORIAS_LEY21719},
                           "medidas_tecnicas": {
                                 "pseudonimizacion": True,
                                 "cifrado_AES256": True,
                                 "audit_log_inmutable": True,
                                 "checkwizard_verificacion": True,
                                 "hitl_decisiones_juridicas": True,

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                           },
                           "transferencias_internacionales": deployment_config.get(
                                 "sub_encargados", []
                           ),
                           "plazo_notificacion_brecha": "72 horas — Art. 38 Ley 21.719",
                    }
                    return dpa

     8. Anonymization como Control Técnico y Obligación
     Normativa
     El Anonymization Audit Student Packet (Pavuluri, 2026) proporciona el marco pedagógico más
     preciso disponible para el análisis de anonimización en contextos legales. Su metodología —
     distinguir entre identificadores directos, detalles sensibles trazables, y hechos jurídicamente útiles—
     es exactamente el framework que implementa el módulo de pseudonimización de Gobernador IA.

     La Ley 21.719, en su Art. 2 letra h), define dato personal como "cualquier información vinculada o
     que pueda vincularse a una o más personas naturales, determinadas o determinables". El concepto
     de determinabilidad es crítico: datos que individualmente no identifican a una persona pueden
     hacerlo en combinación (re-identification risk).

     Gobernador IA implementa un pipeline de anonimización diferencial basado en tres capas:

     Capa A — Eliminación de identificadores directos: RUT, nombre completo, dirección, número de
     teléfono, correo electrónico, número de cuenta. Reemplazados por hashes SHA-256 con salt
     dinámico por tenant.

     Capa B — Generalización de detalles trazables: Fechas exactas convertidas a períodos (semana,
     mes, trimestre). Montos exactos convertidos a rangos. Ubicaciones específicas generalizadas a
     región o zona.

     Capa C — Evaluación de riesgo de re-identificación: Gobernador IA ejecuta un análisis de k-
     anonimato sobre cada dataset antes de permitir su uso para entrenamiento de modelos o análisis
     estadístico. Si k < 5 (menos de 5 individuos comparten el mismo perfil de atributos quasi-
     identificadores), el dataset se bloquea automáticamente.

        # k-Anonymity Evaluator — Gobernador IA
        import pandas as pd

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

        from typing import List

        class KAnonymityEvaluator:
                """
                Evaluador de k-anonimato.
                Base normativa: Art. 2 h) Ley 21.719 (determinabilidad).
                ISO/IEC 42001:2023: Control A.8.4 (gestión de datos para IA).
                Pavuluri (2026): Framework de auditoría de anonimización.
                """

                MINIMUM_K = 5         # Umbral mínimo: GDPR Recital 26, práctica estándar

                def __init__(self, quasi_identifiers: List[str]):
                      self.quasi_identifiers = quasi_identifiers

                def evaluate(self, df: pd.DataFrame) -> dict:
                      """
                      Retorna nivel de k-anonimato y registros en riesgo.
                      Si k < MINIMUM_K, bloquea liberación del dataset.
                      """
                      groups = df.groupby(self.quasi_identifiers).size()
                      min_k = groups.min()
                      records_at_risk = int((groups < self.MINIMUM_K).sum())

                      return {
                            "k_actual": int(min_k),
                            "k_minimo_requerido": self.MINIMUM_K,
                            "cumple": min_k >= self.MINIMUM_K,
                            "registros_en_riesgo": records_at_risk,
                            "decision": "APROBADO" if min_k >= self.MINIMUM_K else "BLOQUEADO",
                            "norma_aplicable": "Art. 2 h) Ley 21.719 + ISO/IEC 42001:2023 A.8.4",
                      }

     La conexión con el ejercicio pedagógico de Pavuluri (2026) es directa: el estudiante que sanitiza un
     correo electrónico de cliente antes de ingresarlo a una IA pública está ejecutando manualmente el
     mismo proceso que Gobernador IA automatiza en escala empresarial. La distinción entre "qué
     necesita la IA para ser útil" y "qué no debe saber la IA para proteger al titular" es la tensión
     operacional central de todo sistema de compliance de datos en IA.

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     9. Responsible AI Use Planning: Marco Pedagógico
     Integrado

     El Responsible AI Use Planning Guide (Pavuluri, 2026) estructural nueve preguntas de
     planificación antes de cualquier uso de IA. Este framework, diseñado para investigación jurídica
     aumentada por IA, tiene una correspondencia directa con los principios de la Ley 21.719 y con la
     arquitectura de Gobernador IA:

             Pregunta Pavuluri                       Principio Ley 21.719                     Implementación Gobernador IA

                                              Art. 12 (finalidad                             Campo finalidad en
       ¿Por qué uso IA aquí?
                                              determinada)                                   RegistroTratamiento

       ¿Qué rol debe jugar la                 Art. 54-55 (decisiones
                                                                                             Clasificador HITL en CheckWizard
       IA?                                    automatizadas)

       ¿Qué información                       Art. 4 (datos mínimos
                                                                                             Pipeline de anonimización por capa
       comparto?                              necesarios)

       ¿Qué supuestos traigo?                 Art. 15 (EIPD)                                 Evaluador de riesgo pre-despliegue

       ¿Qué instrucciones                     Art. 14 (registro de                           System prompt auditado en
       necesita?                              actividades)                                   OpenFang

                                              Art. 32 (medidas de
       ¿Qué riesgos gestiono?                                                                CheckWizard + reglas por artículo
                                              seguridad)

       ¿Qué estrategia de
                                              Art. 14 bis (accountability)                   Compliance report por período
       verificación?

       ¿Qué hago con el                       Art. 54-55 (supervisión
                                                                                             HITL gate antes de acción final
       output?                                humana)

       ¿Qué documento?                        Art. 14 (registro)                             Audit ledger inmutable en Rust

     Esta correspondencia no es casual. Ambos marcos —el pedagógico de Pavuluri y el normativo de la
     Ley 21.719— parten del mismo principio: el uso de IA no transfiere la responsabilidad
     profesional o legal al sistema; la amplifica hacia el humano que lo despliega.

     10. Arquitectura de Evidencia: Trazabilidad Inmutable como
     Prueba Legal
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     En el sistema de responsabilidad civil chileno, la carga de la prueba en materias de protección de
     datos recae sobre el responsable del tratamiento (Art. 14 bis Ley 21.719, principio de
     accountability inverso). Esto significa que ante una reclamación ante la APDP o una demanda civil,
     el responsable debe probar que cumplió, no que el denunciante pruebe que no cumplió.

     Gobernador IA diseña su arquitectura de evidencia para satisfacer exactamente este estándar
     probatorio. El audit ledger de CheckWizard implementa tres propiedades de evidencia legal:

     Propiedad 1 — Inmutabilidad: La cadena de hashes blockchain-style hace computacionalmente
     inviable modificar un registro sin invalidar todos los registros posteriores. Esto satisface el estándar
     de evidencia digital auténtica del Art. 348 bis del Código de Procedimiento Civil.

     Propiedad 2 — Completitud: Cada operación de tratamiento genera un registro con: base de
     licitud, finalidad, categorías de datos, responsable, sub-encargados, timestamp de inicio y fin, y
     hash de integridad. No existe operación sin registro.

     Propiedad 3 — Disponibilidad: El sistema genera un compliance report exportable en formato
     JSON y PDF para uso en procedimientos administrativos ante la APDP o en litigación civil. El
     formato sigue las especificaciones del Reglamento de la APDP (pendiente de publicación, pero
     anticipado por el texto de la Ley 21.719).

        # Generador de evidencia legal — Gobernador IA
        class LegalEvidenceExporter:
                """
                Exporta evidencia de cumplimiento para procedimientos administrativos
                o litigación civil ante APDP o tribunales.
                Base legal: Art. 14 bis Ley 21.719 (accountability inverso).
                """

                def export_for_apdp(
                      self,
                      check_wizard_report: dict,
                      periodo: str,
                      responsable: str
                ) -> dict:
                      return {
                           "documento": "Informe de Cumplimiento — Responsable del Tratamiento",
                           "base_legal": "Art. 14 bis Ley 21.719",
                           "responsable_tratamiento": responsable,
                           "periodo_auditado": periodo,
                           "total_operaciones": check_wizard_report.get("total_records", 0),

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                           "operaciones_conformes": check_wizard_report.get("conformes", 0),
                           "violaciones_detectadas": check_wizard_report.get("violations", []),
                           "medidas_correctivas": check_wizard_report.get("corrective_actions", []),
                           "hash_integridadinformedoc": self._sign_report(check_wizard_report),
                           "generado_por": "Gobernador IA v1.0 — VibeCodingChile SpA",
                           "timestamp_generacion": datetime.utcnow().isoformat(),
                           "nota_legal": (
                                 "Este documento constituye evidencia de las medidas técnicas y "
                                 "organizativas adoptadas por el responsable del tratamiento conforme
                                 "al principio de accountability del Art. 14 bis de la Ley 21.719. "
                                 "Su autenticidad está garantizada por la cadena de hashes "
                                 "inmutables del sistema CheckWizard."
                           ),
                     }

                def _sign_report(self, report: dict) -> str:
                     content = json.dumps(report, sort_keys=True, default=str)
                     return hashlib.sha256(content.encode()).hexdigest()

     11. Modelo de Riesgo Diferenciado por Actor en la Cadena de
     Valor
     Adoptando la matriz de actores del paper IMDA (2026) y aplicándola al contexto normativo chileno,
     se construye el siguiente modelo de riesgo diferenciado:

     11.1 VibeCodingChile como System Provider y Encargado

     Responsabilidades técnicas:

                Diseño y mantenimiento de la arquitectura de tres capas
                Implementación y actualización de las reglas de cumplimiento en CheckWizard
                Pruebas de seguridad y penetration testing periódico
                Divulgación a clientes de las limitaciones del sistema

     Responsabilidades normativas (Ley 21.719):

                DPA suscrito con cada cliente deployer (Art. 14 quáter)
                Medidas de seguridad adecuadas (Art. 32)
                                                                                                      

                Notificación de brechas en 72 horas (Art. 38)
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                Cooperación con APDP en fiscalizaciones (Art. 49)

     Estándar de cuidado ISO/IEC 42001:2023:

                Mantenimiento del sistema de gestión de IA documentado
                Evaluación de riesgo antes de cada actualización mayor
                Registro de incidentes y acciones correctivas

     11.2 Cliente Deployer como Responsable del Tratamiento

     Responsabilidades bajo Ley 21.719:

                Definición de finalidades legítimas de tratamiento (Art. 12)
                Implementación de procedimientos ARCO para titulares (Art. 11)
                Realización de EIPD para operaciones de alto riesgo (Art. 15)
                Designación de Delegado de Protección de Datos si corresponde (Art. 14 ter)

     Salvaguardas técnicas mínimas requeridas:

                HITL activado para todas las decisiones con efectos jurídicos
                Capacitación del personal en uso responsable del sistema (cf. Pavuluri, 2026: Question 9)
                Monitoreo continuo del dashboard de Gobernador IA

     11.3 Anthropic como Model Developer

     La responsabilidad de Anthropic se limita a las capacidades base del modelo Claude. El paper IMDA
     señala que los desarrolladores de modelos "son los mejor posicionados para configurar las
     capacidades y propiedades de seguridad del agente pero tienen visibilidad limitada sobre cómo el
     agente será eventualmente usado". En términos de la Ley 21.719, Anthropic no actúa como
     responsable ni encargado del tratamiento respecto a los datos procesados por los clientes de
     Gobernador IA —su rol es el de proveedor de infraestructura de IA con sus propias obligaciones
     contractuales vía API Terms of Service.

     12. NORMA: Agente Conversacional como Interfaz de
     Gobernanza
     NORMA (Normative Orchestration & Regulatory Monitoring Agent) es el agente conversacional de
     Gobernador IA que actúa como interfaz de compliance para usuarios no técnicos: directores,
     abogados corporativos, DPOs, y auditores.

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     NORMA implementa los siguientes flujos de gobernanza:

     Flujo 1 — Consulta normativa: El usuario pregunta "¿Estamos cumpliendo el Art. 12 de la Ley
     21.719?" NORMA consulta el compliance report de CheckWizard, identifica las operaciones sin base
     de licitud documentada, y genera un reporte ejecutivo con recomendaciones específicas.

     Flujo 2 — Ejercicio de derechos ARCO: Un titular de datos ejerce su derecho de acceso. NORMA
     coordina la búsqueda en el audit ledger, genera el reporte de operaciones de tratamiento
     vinculadas al titular (usando el hash del RUT como clave), y prepara la respuesta dentro del plazo
     de 15 días hábiles del Art. 11 Ley 21.719.

     Flujo 3 — Evaluación de nuevo procesamiento: El cliente desea implementar un nuevo proceso
     que involucra datos personales. NORMA ejecuta la EIPD automática, clasifica el riesgo según la
     matriz Ley 21.719 + EU AI Act, e identifica las salvaguardas técnicas requeridas antes de autorizar el
     despliegue.

     Flujo 4 — Preparación de auditoría APDP: Ante una fiscalización de la Agencia de Protección de
     Datos Personales, NORMA coordina la generación del paquete completo de evidencia: registros de
     tratamiento, compliance reports por período, actas de EIPD realizadas, y el DPA vigente. Todo
     dentro del plazo de respuesta que establezca la APDP.

     La analogía con el Responsable AI Use Planning Guide de Pavuluri (2026) es que NORMA actúa
     exactamente como el framework de planificación: antes de ejecutar cualquier procesamiento
     nuevo, guía al usuario a través de las nueve preguntas críticas y documenta las respuestas como
     parte del registro de actividades de tratamiento.

     13. Conclusiones y Líneas de Desarrollo

     13.1 La Tesis Central Validada

     Este análisis demuestra que la arquitectura de Gobernador IA no es un sistema de compliance
     sobre el desarrollo —es el desarrollo mismo expresado como compliance. Cada decisión
     arquitectónica tiene una correspondencia normativa directa:

                OpenFang/Python implementa los Arts. 12, 11, 14 y 15 de la Ley 21.719
                CheckWizard/Rust implementa el Art. 14 bis (accountability), Art. 32 (seguridad) y la Sección
                9.1 de ISO/IEC 42001:2023
                React Dashboard implementa la transparencia del Art. 13 Ley 21.719 y el Control A.3.2
                ISO/IEC 42001:2023

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                NORMA implementa el derecho a información del Art. 3 Ley 21.719 y el art. 13 EU AI Act

     13.2 Posicionamiento ante la APDP

     La Agencia de Protección de Datos Personales comenzará sus operaciones plenas en 2026. Las
     primeras investigaciones se centrarán en:

          1. Empresas sin registro de actividades de tratamiento (Art. 14)
          2. Organizaciones sin procedimientos ARCO operacionales (Art. 11)
          3. Procesadores sin DPA formalizado (Art. 14 quáter)
          4. Sistemas de IA que toman decisiones automatizadas sin HITL documentado (Art. 54-55)

     Gobernador IA cubre los cuatro frentes desde el primer día de despliegue.

     13.3 La Pregunta Abierta: Responsabilidad por Comportamiento Imprevisible

     El análisis IMDA (2026) identifica como pregunta sin resolver: "¿Quién soporta la responsabilidad
     por acciones imprevisibles del agente?" En el derecho chileno, la respuesta provisional —hasta que
     la APDP o los tribunales generen jurisprudencia— es: el responsable del tratamiento, con la
     posibilidad de repetir en contra del encargado si la causa del daño se origina en una falla del
     sistema encargado.

     Gobernador IA mitiga este riesgo a través de la evidencia pre-generada: el responsable puede
     demostrar qué salvaguardas estaban activas en el momento del incidente, trasladando la carga de
     la prueba al cuestionamiento de si esas salvaguardas eran suficientes dado el contexto, no si
     existían.

     13.4 Líneas de Desarrollo Futuras

     Corto plazo (Q3 2026):

                Integración de la Ley 21.663 (Ciberseguridad) en el módulo de incidentes de CheckWizard
                Generador automático de EIPD con scoring cuantitativo de riesgo
                API REST de NORMA para integración con sistemas legales externos

     Mediano plazo (2027):

                Módulo de cumplimiento EU AI Act para operaciones transfronterizas
                Certificación Gobernador IA bajo ISO/IEC 42001:2023 por organismo acreditado
                Integración con el registro público de la APDP cuando entre en operación

     Largo plazo (2028+):
3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

                Expansión a marcos LATAM: Ley 1581 Colombia, LGPD Brasil, Ley de IA México (proyectada)
                Soporte multi-jurisdicción con resolución automática de conflictos normativos

     14. Referencias Normativas y Técnicas

     Normativa chilena

                Ley 21.719 — Ley sobre Protección de los Datos Personales, D.O. 13.01.2025
                Ley 19.628 — Sobre Protección de la Vida Privada (vigente en lo no derogado), Arts. 54-55
                Ley 21.663 — Ley Marco de Ciberseguridad e Infraestructura Crítica de la Información, 2024
                Código Civil de Chile — Arts. 2.309 y siguientes (responsabilidad extracontractual)
                Código de Procedimiento Civil — Art. 348 bis (evidencia digital)

     Normativa internacional comparada

                Reglamento (UE) 2024/1689 — EU Artificial Intelligence Act, vigente agosto 2024
                Reglamento (UE) 2016/679 — GDPR, Recitales 26 y 75, Arts. 5, 25, 35

     Estándares técnicos

                ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management
                system
                ISO/IEC 27001:2022 — Information security management systems
                NIST AI RMF 1.0 (2023) — AI Risk Management Framework

     Literatura técnico-jurídica citada

                IMDA. Legal Responsibility for AI Agents (Discussion Paper). Infocomm Media Development
                Authority, Singapur, mayo 2026.
                Pavuluri, Emily. Responsible AI Use Planning Guide. Teaching AI-Augmented Legal Research,
                v0.1, junio 2026.
                Pavuluri, Emily. Anonymization Audit: Student Information Packet. Teaching AI-Augmented
                Legal Research, v0.1, mayo 2026.
                SAL Law Reform Committee. Report on the Attribution of Civil Liability for Incidents Involving
                Autonomous Cars. Singapore Academy of Law, 2020.
                Quoine Pte Ltd v B2C2 Ltd [2020] SGCA(I) 2.
                OECD. The Agentic AI Landscape and its Conceptual Foundations, 2025.
                WEF. AI Agents in Action: Foundations for Evaluation and Governance, 2025.

3/7/26, 22:51                                                       paper_gobernador_ia_ley21719.md

     Repositorio técnico

                VibeCodingChile / Gobernador IA — Python/OpenFang + Rust/CheckWizard + React
                Código disponible bajo acuerdo de confidencialidad para due diligence

     Este documento constituye análisis técnico-jurídico de carácter académico y comercial. No constituye
     asesoría legal. Para aplicación específica en su organización, consulte con un abogado habilitado.

     VibeCodingChile SpA | vibecodingchile.dev@vibecodingchile.cl | +56 9 2964 8142

     © 2026 Matías Germán Valentín Rojas Faúndez / VibeCodingChile SpA. Todos los derechos
     reservados.

