from string import Template

hardware_template = Template("module uarchitecture {"
                             "    type * = common.*;\n\n"
                             ""
                             "    input spec_enabled : boolean;\n"
                             "    var mem : mem_t;\n"
                             "    var br_pred_state: br_pred_state_t;\n\n"
                             ""
                             "    procedure direct_branch(cond : boolean, pc_if : pc_t, pc_else : pc_t)\n"
                             "        returns (new_pc : pc_t)"
                             "        modifies br_pred_state;\n"
                             "        modifies spec_level;\n"
                             "        modifies spec_pc;\n"
                             "        ${MOD_SPEC_VARS}\n"
                             "    {\n"
                             "        var pred : boolean;\n\n"
                             "        br_pred_state = common.update_br_pred(br_pred_state, cond);\n"
                             "        pred = common.br_pred(br_pred_state, pc);\n\n"
                             "        if (cond) {\n"
                             "            if (spec_enabled && pred) {\n"
                             "                 call save_reg_states(pc_if);\n"
                             "                 spec_level = spec_level + commmon.spec_idx1;\n"
                             "                 pc = pc_else;\n"
                             "             } else {\n"
                             "                 pc = pc_if;\n"
                             "             }\n"
                             "        } else {\n"
                             "            if (spec_enabled && pred) {\n"
                             "                call save_reg_states(pc_else);\n"
                             "                spec_level = spec_level + common.spec_idx1;\n"
                             "                pc = pc_if;\n"
                             "            } else {\n"
                             "                pc = pc_else;\n"
                             "            }\n"
                             "        }\n"
                             "    }\n\n"
                             ""
                             "    procedure indirect_branch()\n"
                             "    {\n"
                             "        //TODO"
                             "    }\n\n"
                             ""
                             "    // Handles walking back misspeculation\n"
                             "    procedure do_resolve()\n"
                             "        modifies mem;\n"
                             "        modifies spec_level;\n"
                             "        ${MOD_VARS}\n"
                             "    {\n"
                             "        var prev_spec_level : spec_idx_t;\n"
                             "        // Non deterministic choice of walkback level\n"
                             "        assume (prev_spec_level == common.walk_back(br_pred_state, pc, spec_level));\n"
                             "        assume (common.spec_idx0 <=_u prev_spec_level && prev_spec_level <_u spec_level);\n"
                             "        // Walkback\n"
                             "        spec_level = prev_spec_level;\n"
                             "        call restore_state();\n"
                             "    }\n\n"
                             ""
                             "    // Add speculation checkpoint to speculation checkpoint stack\n"
                             "    procedure save_reg_states(resolve_pc : pc_t)\n"
                             "        modifies spec_pc;\n"
                             "        ${MOD_SPEC_VARS}\n"
                             "    {\n"
                             "        ${SAVE_STMTS}\n"
                             "        spec_pc[spec_level] = resolve_pc;\n"
                             "        spec_mem[spec_level] = mem;\n"
                             "    }\n\n"
                             ""
                             "    procedure restore_state()\n"
                             "        modifies pc;\n"
                             "        ${MOD_VARS}\n"
                             "    {\n"
                             "        {RESTORE_STMTS}\n"
                             "        pc = spec_pc[spec_level];\n"
                             "        mem = spec_mem[spec_level];\n"
                             "    }\n\n"
                             ""
                             "    procedure load_mem(addr : word_t)\n"
                             "        returns (value : word_t)\n"
                             "    {\n"
                             "        value = common.read(mem, addr);\n"
                             "    }\n"
                             ""
                             "    procedure store_mem(addr : word_t, value : word_t)\n"
                             "        modifies mem;\n"
                             "    {\n"
                             "        mem = common.write(mem, adr, value);\n"
                             "        assume (common.read(mem, addr) == value);\n"
                             "        assume (forall (addr_ : addr_t) :: addr_ != addr ==> common.read(old_mem, addr_) == common.read(mem, addr_));\n"
                             "    }\n\n"       
                             "}")