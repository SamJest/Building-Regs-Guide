export const PROJECT_REQUIREMENT_MATRIX = [
  {
    "project_id": "single_storey_extension",
    "project": "Single-storey extension",
    "needs_regs_default": "yes",
    "planning_overlap": "often",
    "preferred_route": "full_plans_for_complex_or_large; building_notice_for_simple_domestic_when_allowed",
    "approved_documents": [
      "A",
      "B",
      "C",
      "F",
      "G",
      "H",
      "K",
      "L",
      "M",
      "O"
    ],
    "evidence": [
      "existing and proposed plans",
      "structural calculations if openings/steelwork/foundations",
      "drainage layout",
      "insulation and energy details",
      "fire safety and escape notes",
      "ventilation strategy"
    ],
    "inspection_stages": [
      "commencement",
      "foundation excavation",
      "foundation concrete",
      "oversite/dpc",
      "drainage before cover",
      "structural steel/beams",
      "insulation before cover",
      "roof structure",
      "final completion"
    ],
    "red_flags": [
      "building over or near drains",
      "large glazed areas",
      "open-plan layout affecting escape",
      "party wall matters",
      "sewer build-over agreement may be separate"
    ]
  },
  {
    "project_id": "two_storey_extension",
    "project": "Two-storey extension",
    "needs_regs_default": "yes",
    "planning_overlap": "usually",
    "preferred_route": "full_plans",
    "approved_documents": [
      "A",
      "B",
      "C",
      "F",
      "G",
      "H",
      "K",
      "L",
      "M",
      "O"
    ],
    "evidence": [
      "full architectural drawings",
      "structural design",
      "foundation design",
      "drainage design",
      "fire escape and smoke alarm strategy",
      "energy calculations/details"
    ],
    "inspection_stages": [
      "commencement",
      "foundations",
      "drainage",
      "structural frame",
      "upper floor/roof structure",
      "fire stopping",
      "insulation",
      "final completion"
    ],
    "red_flags": [
      "stair/landing protection",
      "means of escape from upper floors",
      "soil conditions/trees",
      "overlooking/planning separate"
    ]
  },
  {
    "project_id": "loft_conversion",
    "project": "Loft conversion",
    "needs_regs_default": "yes",
    "planning_overlap": "sometimes",
    "preferred_route": "full_plans",
    "approved_documents": [
      "A",
      "B",
      "F",
      "K",
      "L",
      "M",
      "P"
    ],
    "evidence": [
      "structural calculations for floor/roof changes",
      "fire safety strategy",
      "stairs layout",
      "insulation and ventilation details",
      "roof window/dormer drawings"
    ],
    "inspection_stages": [
      "commencement",
      "structural steels/floor joists",
      "fire protection before cover",
      "insulation",
      "stair installation",
      "final completion"
    ],
    "red_flags": [
      "protected stair route",
      "doors/smoke alarms",
      "head height",
      "neighbouring chimney/party wall",
      "dormer planning rules separate"
    ]
  },
  {
    "project_id": "garage_conversion",
    "project": "Garage conversion",
    "needs_regs_default": "yes",
    "planning_overlap": "sometimes",
    "preferred_route": "building_notice_possible_but_full_plans_better_for_uncertainty",
    "approved_documents": [
      "A",
      "B",
      "C",
      "F",
      "L",
      "M",
      "P"
    ],
    "evidence": [
      "floor insulation/moisture details",
      "wall and roof insulation details",
      "ventilation strategy",
      "new openings lintel details",
      "fire separation where attached"
    ],
    "inspection_stages": [
      "commencement",
      "floor build-up before cover",
      "damp proofing",
      "insulation",
      "new openings/structure",
      "final completion"
    ],
    "red_flags": [
      "garage floor level/damp",
      "former vehicle door infill",
      "escape window/light/ventilation",
      "parking condition under planning"
    ]
  },
  {
    "project_id": "load_bearing_wall_removal",
    "project": "Removing a load-bearing wall",
    "needs_regs_default": "yes",
    "planning_overlap": "rarely unless listed/structural external changes",
    "preferred_route": "building_notice_possible_if_simple; full_plans_for_complex",
    "approved_documents": [
      "A",
      "B",
      "K"
    ],
    "evidence": [
      "structural engineer calculations",
      "beam specification",
      "padstone/bearing details",
      "method/support sequence",
      "fire protection to steel where required"
    ],
    "inspection_stages": [
      "before works/open-up",
      "beam/steel before cover",
      "fire protection before cover",
      "completion"
    ],
    "red_flags": [
      "party wall",
      "chimney support",
      "open-plan fire escape impact",
      "work started without inspection"
    ]
  },
  {
    "project_id": "chimney_breast_removal",
    "project": "Chimney breast removal",
    "needs_regs_default": "yes_if_structural",
    "planning_overlap": "possible in listed/conservation/external stack changes",
    "preferred_route": "full_plans_or_building_notice_with_structural_calcs",
    "approved_documents": [
      "A",
      "B"
    ],
    "evidence": [
      "structural calculations",
      "support details/gallows bracket suitability where allowed",
      "neighbour/party wall evidence",
      "fire stopping details"
    ],
    "inspection_stages": [
      "open-up",
      "support installation",
      "fire stopping/making good",
      "completion"
    ],
    "red_flags": [
      "shared chimney stack",
      "removed lower breast with stack above",
      "listed building consent separate"
    ]
  },
  {
    "project_id": "bathroom_installation",
    "project": "Installing a new bathroom",
    "needs_regs_default": "yes_if_new_drainage_plumbing_or_electrics",
    "planning_overlap": "rarely",
    "preferred_route": "competent_person_for_electrics_where_possible; building_control_if_new_drainage_or_notifiable_work",
    "approved_documents": [
      "F",
      "G",
      "H",
      "P"
    ],
    "evidence": [
      "drainage route",
      "ventilation extract details",
      "hot water/scalding notes",
      "electrical certificate if applicable"
    ],
    "inspection_stages": [
      "drainage before cover",
      "ventilation duct route",
      "electrical certification",
      "completion"
    ],
    "red_flags": [
      "electrics near bath/shower",
      "new soil pipe route",
      "poor extract termination",
      "flat lease/freeholder constraints"
    ]
  },
  {
    "project_id": "kitchen_refit",
    "project": "Kitchen refit",
    "needs_regs_default": "sometimes",
    "planning_overlap": "rarely",
    "preferred_route": "competent_person_for_electrics_gas; building_control_if_structural_or_new_drainage",
    "approved_documents": [
      "F",
      "G",
      "H",
      "J",
      "P"
    ],
    "evidence": [
      "gas/electrical certificates",
      "extract ventilation details",
      "drainage changes",
      "structural calculations if wall removed"
    ],
    "inspection_stages": [
      "structure if altered",
      "drainage if altered",
      "services certificates",
      "completion"
    ],
    "red_flags": [
      "load-bearing wall removed during refit",
      "gas appliance/flue changes",
      "new circuits",
      "extract not ducted correctly"
    ]
  },
  {
    "project_id": "replacement_windows_doors",
    "project": "Replacement windows and doors",
    "needs_regs_default": "yes_unless_competent_person_or_exempt_door_cases",
    "planning_overlap": "sometimes in conservation/listed/flats",
    "preferred_route": "competent_person_scheme",
    "approved_documents": [
      "B",
      "F",
      "K",
      "L",
      "M",
      "Q"
    ],
    "evidence": [
      "FENSA/CERTASS or equivalent certificate",
      "safety glazing locations",
      "escape window details where relevant",
      "trickle ventilation/ventilation strategy"
    ],
    "inspection_stages": [
      "usually certified by installer",
      "completion certificate/evidence retained"
    ],
    "red_flags": [
      "removing escape window function",
      "insufficient background ventilation",
      "listed building/conservation area",
      "new opening/lintel needed"
    ]
  },
  {
    "project_id": "electrical_work",
    "project": "Electrical work",
    "needs_regs_default": "sometimes",
    "planning_overlap": "rarely",
    "preferred_route": "registered electrician/competent_person_scheme_for_notifiable_work",
    "approved_documents": [
      "P"
    ],
    "evidence": [
      "electrical installation certificate",
      "building regulations compliance certificate for notifiable work",
      "circuit details"
    ],
    "inspection_stages": [
      "first fix if building control route",
      "test certificate",
      "completion"
    ],
    "red_flags": [
      "bathroom/shower zones",
      "new consumer unit/fuse box",
      "new circuit",
      "DIY work without inspection route"
    ]
  },
  {
    "project_id": "boiler_or_heating_system",
    "project": "Boiler or heating system replacement",
    "needs_regs_default": "yes_unless_competent_person",
    "planning_overlap": "sometimes for flues in sensitive locations",
    "preferred_route": "Gas Safe/OFTEC/HETAS/MCS as relevant",
    "approved_documents": [
      "G",
      "J",
      "L"
    ],
    "evidence": [
      "installer compliance certificate",
      "commissioning certificate",
      "flue location",
      "controls/energy details"
    ],
    "inspection_stages": [
      "usually installer certification",
      "completion certificate/evidence retained"
    ],
    "red_flags": [
      "flue termination near boundary/opening",
      "unvented cylinder",
      "solid fuel appliance",
      "heat pump/noise/planning overlap"
    ]
  },
  {
    "project_id": "roof_covering_replacement",
    "project": "Replacing roof coverings",
    "needs_regs_default": "often_if_significant_or_thermal_element",
    "planning_overlap": "sometimes",
    "preferred_route": "building_control_or_competent_scheme_where_available",
    "approved_documents": [
      "A",
      "C",
      "L"
    ],
    "evidence": [
      "roof covering specification",
      "structural load check if heavier covering",
      "insulation details if thermal upgrade triggered",
      "moisture/ventilation details"
    ],
    "inspection_stages": [
      "before cover",
      "insulation/ventilation",
      "completion"
    ],
    "red_flags": [
      "changing to heavier tiles",
      "condensation risk",
      "conservation/listed restrictions",
      "working at height/contractor competence"
    ]
  },
  {
    "project_id": "solar_panels",
    "project": "Solar panels",
    "needs_regs_default": "yes_for_structural_and_electrical_aspects",
    "planning_overlap": "sometimes/permitted_development_rules_separate",
    "preferred_route": "MCS/electrical competent person plus structural suitability check",
    "approved_documents": [
      "A",
      "B",
      "P"
    ],
    "evidence": [
      "roof structural suitability",
      "electrical certificate",
      "MCS certificate where applicable",
      "fire/service routing notes"
    ],
    "inspection_stages": [
      "installer survey",
      "electrical testing",
      "completion documentation"
    ],
    "red_flags": [
      "weak roof/old roof covering",
      "flat roof ballast loads",
      "battery storage/fire location",
      "listed/conservation planning rules"
    ]
  },
  {
    "project_id": "outbuilding_or_garden_room",
    "project": "Outbuilding or garden room",
    "needs_regs_default": "depends_on_size_sleeping_accommodation_and_services",
    "planning_overlap": "often",
    "preferred_route": "approval_needed_if_sleeping_accommodation_or_over_exemption_thresholds_or_services_complex",
    "approved_documents": [
      "A",
      "B",
      "C",
      "F",
      "H",
      "L",
      "P"
    ],
    "evidence": [
      "size/use statement",
      "sleeping accommodation answer",
      "electrical certification",
      "foundations/floor details",
      "insulation if heated",
      "drainage if plumbing"
    ],
    "inspection_stages": [
      "foundation/base",
      "structure",
      "insulation/services",
      "completion"
    ],
    "red_flags": [
      "used as bedroom/annexe",
      "close to boundary/fire spread",
      "toilet/shower drainage",
      "commercial use"
    ]
  }
];
