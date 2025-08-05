import pandera.pandas as pa
from typing import Optional
from dataclasses import dataclass
from pandera.typing import Series

from .enums import ServerCVar, Scope, NType

@dataclass
class MetaStruct:
    ingame_cvar: ServerCVar
    scope: Scope
    ntype: Optional[NType]

demoparser_schema = pa.DataFrameSchema(
    columns={
        "tick": pa.Column(
            int,
            description="Game tick number",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.net_tick,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "user_id": pa.Column(
            int,
            description="User ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "entity_id": pa.Column(
            int,
            description="Entity ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "player_steamid": pa.Column(
            str,
            description="Player Steam ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_steamID,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "player_name": pa.Column(
            str,
            description="Player name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iszPlayerName,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "player_color": pa.Column(
            int,
            description="Player teammate color",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompTeammateColor,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),

        # Player Demographics & Status - General Information
        "ping": pa.Column(
            int,
            description="Player ping in milliseconds",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iPing,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "score": pa.Column(
            int,
            description="Player score",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iScore,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "mvps": pa.Column(
            int,
            description="Most Valuable Player awards",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iMVPs,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "balance": pa.Column(
            int,
            description="Player money balance",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iAccount,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_connected": pa.Column(
            bool,
            description="Player connection status",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iConnected,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "has_controlled_bot_this_round": pa.Column(
            bool,
            description="Has controlled bot this round",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bHasControlledBotThisRound,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "can_control_bot": pa.Column(
            bool,
            description="Can control observed bot",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bCanControlObservedBot,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_controlling_bot": pa.Column(
            bool,
            description="Is controlling bot",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bControllingBot,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_coach_team": pa.Column(
            int,
            description="Coaching team",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCoachingTeam,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "spotted": pa.Column(
            bool,
            description="Player spotted status",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bSpotted,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "approximate_spotted_by": pa.Column(
            int,
            description="Radar approximate spotted by mask",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bSpottedByMask,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),

        # In-Game Status & State
        "player_state": pa.Column(
            int,
            description="Player state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iPlayerState,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "life_state": pa.Column(
            int,
            description="Life state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_lifeState,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_alive": pa.Column(
            bool,
            description="Player alive status",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bPawnIsAlive,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "health": pa.Column(
            int,
            description="Player health points",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iHealth,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "armor_value": pa.Column(
            int,
            description="Armor value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_ArmorValue,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "moved_since_spawn": pa.Column(
            bool,
            description="Has moved since spawn",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bHasMovedSinceSpawn,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "last_place_name": pa.Column(
            str,
            description="Last place name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szLastPlaceName,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),

        # Player Rank & Match Progression
        "comp_wins": pa.Column(
            int,
            description="Competitive wins",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveWins,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "comp_rank_type": pa.Column(
            int,
            description="Competitive rank type",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveRankType,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "rank": pa.Column(
            int,
            description="Competitive ranking",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveRanking,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "rank_if_win": pa.Column(
            int,
            description="Predicted rank if win",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveRankingPredicted_Win,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "rank_if_loss": pa.Column(
            int,
            description="Predicted rank if loss",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveRankingPredicted_Loss,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "rank_if_tie": pa.Column(
            int,
            description="Predicted rank if tie",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCompetitiveRankingPredicted_Tie,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),

        # Player Positional & Environmental Data
        "X": pa.Column(
            float,
            description="Player X coordinate",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_vec_plus_m_cell,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "Y": pa.Column(
            float,
            description="Player Y coordinate",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_vec_plus_m_cell,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "Z": pa.Column(
            float,
            description="Player Z coordinate",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_vec_plus_m_cell,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "which_bomb_zone": pa.Column(
            int,
            description="Which bomb zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nWhichBombZone,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "in_bomb_zone": pa.Column(
            bool,
            description="In bomb zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInBombZone,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "in_buy_zone": pa.Column(
            bool,
            description="In buy zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInBuyZone,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "in_no_defuse_area": pa.Column(
            bool,
            description="In no defuse area",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInNoDefuseArea,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "in_hostage_rescue_zone": pa.Column(
            bool,
            description="In hostage rescue zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInHostageRescueZone,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),

        # Player Match Data (Round & Game Timings specific to the player)
        "spawn_time": pa.Column(
            int,
            description="Player spawn time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iPawnLifetimeStart,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "death_time": pa.Column(
            int,
            description="Player death time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iPawnLifetimeEnd,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "game_time": pa.Column(
            int,
            description="Game time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.net_tick,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "team_num": pa.Column(
            int,
            description="Team number",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iTeamNum,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "pending_team_num": pa.Column(
            int,
            description="Pending team number",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iPendingTeamNum,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "ever_played_on_team": pa.Column(
            bool,
            description="Ever played on team",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bEverPlayedOnTeam,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),

        # Game State Data (Global to the match/round)
        "team_rounds_total": pa.Column(
            int,
            description="Team total rounds won",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iScore,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "team_surrendered": pa.Column(
            bool,
            description="Team surrendered",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bSurrendered,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_name": pa.Column(
            str,
            description="Team name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szTeamname,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_score_overtime": pa.Column(
            int,
            description="Team overtime score",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_scoreOvertime,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_match_stat": pa.Column(
            str,
            description="Team match stat",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szTeamMatchStat,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_num_map_victories": pa.Column(
            int,
            description="Team map victories",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_numMapVictories,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_score_first_half": pa.Column(
            int,
            description="Team first half score",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_scoreFirstHalf,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_score_second_half": pa.Column(
            int,
            description="Team second half score",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_scoreSecondHalf,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "team_clan_name": pa.Column(
            str,
            description="Team clan name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szClanTeamname,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "ct_losing_streak": pa.Column(
            int,
            description="CT consecutive losses",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iNumConsecutiveCTLoses,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "t_losing_streak": pa.Column(
            int,
            description="Terrorist consecutive losses",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iNumConsecutiveTerroristLoses,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "n_best_of_maps": pa.Column(
            int,
            description="Number of best of maps",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_numBestOfMaps,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),

        # Aggregate Statistics (Match-level totals)
        "kills_total": pa.Column(
            int,
            description="Total kills",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iKills,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "headshot_kills_total": pa.Column(
            int,
            description="Total headshot kills",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iHeadShotKills,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "deaths_total": pa.Column(
            int,
            description="Total deaths",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iDeaths,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "assists_total": pa.Column(
            int,
            description="Total assists",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iAssists,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "alive_time_total": pa.Column(
            int,
            description="Total alive time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iLiveTime,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "ace_rounds_total": pa.Column(
            int,
            description="Total ace rounds (5 kills)",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEnemy5Ks,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "four_k_rounds_total": pa.Column(
            int,
            description="Total 4-kill rounds",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEnemy4Ks,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "three_k_rounds_total": pa.Column(
            int,
            description="Total 3-kill rounds",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEnemy3Ks,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "damage_total": pa.Column(
            int,
            description="Total damage dealt",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iDamage,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "objective_total": pa.Column(
            int,
            description="Total objective score",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iObjective,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "utility_damage_total": pa.Column(
            int,
            description="Total utility damage",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iUtilityDamage,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "enemies_flashed_total": pa.Column(
            int,
            description="Total enemies flashed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEnemiesFlashed,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "equipment_value_total": pa.Column(
            int,
            description="Total equipment value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEquipmentValue,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "money_saved_total": pa.Column(
            int,
            description="Total money saved",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iMoneySaved,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "kill_reward_total": pa.Column(
            int,
            description="Total kill reward",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iKillReward,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "cash_earned_total": pa.Column(
            int,
            description="Total cash earned",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCashEarned,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        
        # Additional Player Status & Actions
        "shots_fired": pa.Column(
            int,
            description="Number of shots fired",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iShotsFired,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "resume_zoom": pa.Column(
            bool,
            description="Resume zoom after reload",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bResumeZoom,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "molotov_damage_time": pa.Column(
            float,
            description="Molotov damage time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fMolotovDamageTime,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "killed_by_taser": pa.Column(
            bool,
            description="Killed by taser",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bKilledByTaser,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "blocking_use_in_progess": pa.Column(
            int,
            description="Blocking use action in progress",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iBlockingUseActionInProgress,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "leader_honors": pa.Column(
            int,
            description="Leadership commendations",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nPersonaDataPublicCommendsLeader,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "teacher_honors": pa.Column(
            int,
            description="Teaching commendations",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nPersonaDataPublicCommendsTeacher,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "friendly_honors": pa.Column(
            int,
            description="Friendly commendations",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nPersonaDataPublicCommendsFriendly,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "passive_items": pa.Column(
            str,
            description="Passive items",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_passiveItems,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_scoped": pa.Column(
            bool,
            description="Player is scoped",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsScoped,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_walking": pa.Column(
            bool,
            description="Player is walking",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsWalking,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_auto_muted": pa.Column(
            bool,
            description="Has communication abuse mute",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bHasCommunicationAbuseMute,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "is_rescuing": pa.Column(
            bool,
            description="Player is rescuing hostage",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsRescuing,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_defusing": pa.Column(
            bool,
            description="Player is defusing bomb",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsDefusing,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_grabbing_hostage": pa.Column(
            bool,
            description="Player is grabbing hostage",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsGrabbingHostage,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        
        # Player Movement Data
        "move_state": pa.Column(
            int,
            description="Player movement state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iMoveState,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "move_collide": pa.Column(
            int,
            description="Movement collision state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_MoveCollide,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "move_type": pa.Column(
            int,
            description="Movement type",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_MoveType,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "stamina": pa.Column(
            float,
            description="Player stamina",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flStamina,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "direction": pa.Column(
            int,
            description="Player direction",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iDirection,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "max_speed": pa.Column(
            float,
            description="Maximum speed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flMaxspeed,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "velocity": pa.Column(
            float,
            description="Player velocity magnitude",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "velocity_X": pa.Column(
            float,
            description="Player X velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "velocity_Y": pa.Column(
            float,
            description="Player Y velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "velocity_Z": pa.Column(
            float,
            description="Player Z velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "velo_modifier": pa.Column(
            float,
            description="Velocity modifier",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flVelocityModifier,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "allow_auto_movement": pa.Column(
            bool,
            description="Allow automatic movement",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bAllowAutoMovement,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "ground_accel_linear_frac_last_time": pa.Column(
            float,
            description="Ground acceleration linear fraction last time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flGroundAccelLinearFracLastTime,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "is_strafing": pa.Column(
            bool,
            description="Player is strafing",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bStrafing,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "is_airborne": pa.Column(
            bool,
            description="Player is airborne",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_hGroundEntity,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        
        # Ducking Status
        "in_crouch": pa.Column(
            bool,
            description="Player in crouch",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInCrouch,
                scope=Scope.PER_TICK
            )
        ),
        "in_duck_jump": pa.Column(
            bool,
            description="Player in duck jump",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInDuckJump,
                scope=Scope.PER_TICK
            )
        ),
        "crouch_state": pa.Column(
            int,
            description="Crouch state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nCrouchState,
                scope=Scope.PER_TICK
            )
        ),
        "duck_time_ms": pa.Column(
            int,
            description="Duck time in milliseconds",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nDuckTimeMsecs,
                scope=Scope.PER_TICK
            )
        ),
        "duck_amount": pa.Column(
            float,
            description="Duck amount",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flDuckAmount,
                scope=Scope.PER_TICK
            )
        ),
        "duck_speed": pa.Column(
            float,
            description="Duck speed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flDuckSpeed,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "duck_overrdie": pa.Column(
            bool,
            description="Duck override",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bDuckOverride,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "ducked": pa.Column(
            bool,
            description="Player ducked",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bDucked,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "ducking": pa.Column(
            bool,
            description="Player ducking",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bDucking,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "last_duck_time": pa.Column(
            float,
            description="Last duck time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flLastDuckTime,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        
        # Jumping Status
        "max_fall_velo": pa.Column(
            float,
            description="Maximum fall velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flMaxFallVelocity,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "old_jump_pressed": pa.Column(
            bool,
            description="Old jump pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bOldJumpPressed,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "jump_until": pa.Column(
            float,
            description="Jump until time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flJumpUntil,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "jump_velo": pa.Column(
            float,
            description="Jump velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flJumpVel,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "fall_velo": pa.Column(
            float,
            description="Fall velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flFallVelocity,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "jump_time_ms": pa.Column(
            int,
            description="Jump time in milliseconds",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nJumpTimeMsecs,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        
        # Player Aim & Vision Data
        "pitch": pa.Column(
            float,
            description="Player pitch (vertical look angle)",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_angEyeAngles_0,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "yaw": pa.Column(
            float,
            description="Player yaw (horizontal look angle)",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_angEyeAngles_1,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "aim_punch_angle": pa.Column(
            float,
            description="Aim punch angle",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_aimPunchAngle,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "aim_punch_angle_vel": pa.Column(
            float,
            description="Aim punch angle velocity",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_aimPunchAngleVel,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "fov": pa.Column(
            int,
            description="Field of view",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iDesiredFOV,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "crosshair_code": pa.Column(
            str,
            description="Crosshair code",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szCrosshairCodes,
                scope=Scope.GLOBAL,
                ntype=NType.CLIENT
            )
        ),
        
        # Player Flash Data
        "flash_alpha": pa.Column(
            float,
            description="Flash alpha level",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "flash_duration": pa.Column(
            float,
            description="Flash duration",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flFlashDuration,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        "flash_max_alpha": pa.Column(
            float,
            description="Flash maximum alpha",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flFlashMaxAlpha,
                scope=Scope.PER_TICK,
                ntype=NType.ENGINE
            )
        ),
        
        # Player Economy & Equipment
        "has_defuser": pa.Column(
            bool,
            description="Player has defuse kit",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bPawnHasDefuser,
                scope=Scope.PER_TICK
            )
        ),
        "has_helmet": pa.Column(
            bool,
            description="Player has helmet",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bPawnHasHelmet,
                scope=Scope.PER_TICK
            )
        ),
        "start_balance": pa.Column(
            int,
            description="Starting round balance",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iStartAccount,
                scope=Scope.PER_ROUND
            )
        ),
        "total_cash_spent": pa.Column(
            int,
            description="Total cash spent in match",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iTotalCashSpent,
                scope=Scope.GLOBAL
            )
        ),
        "cash_spent_this_round": pa.Column(
            int,
            description="Cash spent this round",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iCashSpentThisRound,
                scope=Scope.PER_ROUND
            )
        ),
        "round_start_equip_value": pa.Column(
            int,
            description="Round start equipment value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_unRoundStartEquipmentValue,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        "current_equip_value": pa.Column(
            int,
            description="Current equipment value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_unCurrentEquipmentValue,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "weapon_purchases_this_match": pa.Column(
            int,
            description="Weapon purchases this match",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iWeaponPurchasesThisMatch,
                scope=Scope.GLOBAL,
                ntype=NType.SERVER
            )
        ),
        "weapon_purchases_this_round": pa.Column(
            int,
            description="Weapon purchases this round",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iWeaponPurchasesThisRound,
                scope=Scope.PER_ROUND,
                ntype=NType.SERVER
            )
        ),
        
        # Player Inventory & Cosmetics
        "inventory": pa.Column(
            str,
            description="Player inventory",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "inventory_as_ids": pa.Column(
            str,
            description="Player inventory as IDs",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.SERVER
            )
        ),
        "music_kit_id": pa.Column(
            int,
            description="Music kit ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_unMusicID,
                scope=Scope.GLOBAL
            )
        ),
        "agent_skin": pa.Column(
            str,
            description="Agent skin",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL
            )
        ),
        "glove_paint_id": pa.Column(
            int,
            description="Glove paint ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL
            )
        ),
        "glove_paint_seed": pa.Column(
            int,
            description="Glove paint seed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL
            )
        ),
        "glove_paint_float": pa.Column(
            float,
            description="Glove paint float",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL
            )
        ),
        "glove_item_idx": pa.Column(
            int,
            description="Glove item index",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.GLOBAL
            )
        ),
        
        # Player Injury & Combat State
        "next_attack_time": pa.Column(
            float,
            description="Next attack time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flNextAttack,
                scope=Scope.PER_TICK
            )
        ),
        "time_last_injury": pa.Column(
            float,
            description="Time of last injury",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flTimeOfLastInjury,
                scope=Scope.PER_TICK
            )
        ),
        "direction_last_injury": pa.Column(
            int,
            description="Direction of last injury",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nRelativeDirectionOfLastInjury,
                scope=Scope.PER_TICK
            )
        ),
        "wait_for_no_attack": pa.Column(
            bool,
            description="Wait for no attack",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bWaitForNoAttack,
                scope=Scope.PER_TICK
            )
        ),
        
        # Player Button Press Data
        "buttons": pa.Column(
            int,
            description="Button down mask",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "FORWARD": pa.Column(
            bool,
            description="Forward button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "LEFT": pa.Column(
            bool,
            description="Left button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "RIGHT": pa.Column(
            bool,
            description="Right button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "BACK": pa.Column(
            bool,
            description="Back button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "FIRE": pa.Column(
            bool,
            description="Fire button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "RIGHTCLICK": pa.Column(
            bool,
            description="Right click button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "RELOAD": pa.Column(
            bool,
            description="Reload button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "INSPECT": pa.Column(
            bool,
            description="Inspect button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "USE": pa.Column(
            bool,
            description="Use button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "ZOOM": pa.Column(
            bool,
            description="Zoom button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "SCOREBOARD": pa.Column(
            bool,
            description="Scoreboard button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "WALK": pa.Column(
            bool,
            description="Walk button pressed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nButtonDownMaskPrev,
                scope=Scope.PER_TICK
            )
        ),
        
        # Enhanced Game State Data
        "terrorist_cant_buy": pa.Column(
            bool,
            description="Terrorists cannot buy",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bTCantBuy,
                scope=Scope.PER_ROUND
            )
        ),
        "ct_cant_buy": pa.Column(
            bool,
            description="Counter-Terrorists cannot buy",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bCTCantBuy,
                scope=Scope.PER_ROUND
            )
        ),
        "is_freeze_period": pa.Column(
            bool,
            description="Is freeze period",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bFreezePeriod,
                scope=Scope.PER_ROUND
            )
        ),
        "is_warmup_period": pa.Column(
            bool,
            description="Is warmup period",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bWarmupPeriod,
                scope=Scope.GLOBAL
            )
        ),
        "warmup_period_end": pa.Column(
            float,
            description="Warmup period end time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fWarmupPeriodEnd,
                scope=Scope.GLOBAL
            )
        ),
        "warmup_period_start": pa.Column(
            float,
            description="Warmup period start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fWarmupPeriodStart,
                scope=Scope.GLOBAL
            )
        ),
        "is_terrorist_timeout": pa.Column(
            bool,
            description="Terrorist timeout active",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bTerroristTimeOutActive,
                scope=Scope.PER_ROUND
            )
        ),
        "is_ct_timeout": pa.Column(
            bool,
            description="Counter-Terrorist timeout active",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bCTTimeOutActive,
                scope=Scope.PER_ROUND
            )
        ),
        "terrorist_timeout_remaining": pa.Column(
            float,
            description="Terrorist timeout remaining",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flTerroristTimeOutRemaining,
                scope=Scope.PER_ROUND
            )
        ),
        "ct_timeout_remaining": pa.Column(
            float,
            description="Counter-Terrorist timeout remaining",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flCTTimeOutRemaining,
                scope=Scope.PER_ROUND
            )
        ),
        "num_terrorist_timeouts": pa.Column(
            int,
            description="Number of terrorist timeouts",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nTerroristTimeOuts,
                scope=Scope.GLOBAL
            )
        ),
        "num_ct_timeouts": pa.Column(
            int,
            description="Number of CT timeouts",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nCTTimeOuts,
                scope=Scope.GLOBAL
            )
        ),
        "is_technical_timeout": pa.Column(
            bool,
            description="Technical timeout active",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bTechnicalTimeOut,
                scope=Scope.PER_ROUND
            )
        ),
        "is_waiting_for_resume": pa.Column(
            bool,
            description="Match waiting for resume",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bMatchWaitingForResume,
                scope=Scope.GLOBAL
            )
        ),
        "match_start_time": pa.Column(
            float,
            description="Match start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fMatchStartTime,
                scope=Scope.GLOBAL
            )
        ),
        "round_start_time": pa.Column(
            float,
            description="Round start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fRoundStartTime,
                scope=Scope.PER_ROUND
            )
        ),
        "restart_round_time": pa.Column(
            float,
            description="Restart round time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flRestartRoundTime,
                scope=Scope.PER_ROUND
            )
        ),
        "is_game_restart": pa.Column(
            bool,
            description="Game restart flag",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bGameRestart,
                scope=Scope.GLOBAL
            )
        ),
        "game_start_time": pa.Column(
            float,
            description="Game start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flGameStartTime,
                scope=Scope.GLOBAL
            )
        ),
        "time_until_next_phase_start": pa.Column(
            float,
            description="Time until next phase starts",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_timeUntilNextPhaseStarts,
                scope=Scope.PER_ROUND
            )
        ),
        "game_phase": pa.Column(
            int,
            description="Current game phase",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_gamePhase,
                scope=Scope.PER_ROUND
            )
        ),
        "total_rounds_played": pa.Column(
            int,
            description="Total rounds played",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_totalRoundsPlayed,
                scope=Scope.GLOBAL
            )
        ),
        "rounds_played_this_phase": pa.Column(
            int,
            description="Rounds played this phase",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nRoundsPlayedThisPhase,
                scope=Scope.GLOBAL
            )
        ),
        "round_in_progress": pa.Column(
            bool,
            description="Round in progress",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bRoundInProgress,
                scope=Scope.PER_ROUND
            )
        ),
        
        # Objective & Game Mode
        "hostages_remaining": pa.Column(
            int,
            description="Hostages remaining",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iHostagesRemaining,
                scope=Scope.PER_ROUND
            )
        ),
        "any_hostages_reached": pa.Column(
            bool,
            description="Any hostages reached",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bAnyHostageReached,
                scope=Scope.PER_ROUND
            )
        ),
        "has_bombites": pa.Column(
            bool,
            description="Map has bomb sites",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bMapHasBombTarget,
                scope=Scope.GLOBAL
            )
        ),
        "has_rescue_zone": pa.Column(
            bool,
            description="Map has rescue zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bMapHasRescueZone,
                scope=Scope.GLOBAL
            )
        ),
        "has_buy_zone": pa.Column(
            bool,
            description="Map has buy zone",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bMapHasBuyZone,
                scope=Scope.GLOBAL
            )
        ),
        "is_bomb_dropped": pa.Column(
            bool,
            description="Bomb is dropped",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bBombDropped,
                scope=Scope.PER_ROUND
            )
        ),
        "is_bomb_planted": pa.Column(
            bool,
            description="Bomb is planted",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bBombPlanted,
                scope=Scope.PER_ROUND
            )
        ),
        "round_win_status": pa.Column(
            int,
            description="Round win status",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRoundWinStatus,
                scope=Scope.PER_ROUND
            )
        ),
        "round_win_reason": pa.Column(
            int,
            description="Round win reason",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_eRoundWinReason,
                scope=Scope.PER_ROUND
            )
        ),
        "is_matchmaking": pa.Column(
            bool,
            description="Is matchmaking game",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsQueuedMatchmaking,
                scope=Scope.GLOBAL
            )
        ),
        "match_making_mode": pa.Column(
            int,
            description="Matchmaking mode",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nQueuedMatchmakingMode,
                scope=Scope.GLOBAL
            )
        ),
        "is_valve_dedicated_server": pa.Column(
            bool,
            description="Is Valve dedicated server",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsValveDS,
                scope=Scope.GLOBAL
            )
        ),
        "gungame_prog_weap_ct": pa.Column(
            int,
            description="Gun game progressive weapons CT",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iNumGunGameProgressiveWeaponsCT,
                scope=Scope.GLOBAL
            )
        ),
        "gungame_prog_weap_t": pa.Column(
            int,
            description="Gun game progressive weapons T",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iNumGunGameProgressiveWeaponsT,
                scope=Scope.GLOBAL
            )
        ),
        "spectator_slot_count": pa.Column(
            int,
            description="Spectator slot count",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iSpectatorSlotCount,
                scope=Scope.GLOBAL
            )
        ),
        "is_match_started": pa.Column(
            bool,
            description="Match has started",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bHasMatchStarted,
                scope=Scope.GLOBAL
            )
        ),
        "survival_start_time": pa.Column(
            float,
            description="Survival start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flSurvivalStartTime,
                scope=Scope.GLOBAL
            )
        ),
        
        # Weapon Data (Currently Equipped Weapon)
        "active_weapon": pa.Column(
            str,
            description="Active weapon handle",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_hActiveWeapon,
                scope=Scope.PER_TICK
            )
        ),
        "active_weapon_name": pa.Column(
            str,
            description="Active weapon name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iItemDefinitionIndex,
                scope=Scope.PER_TICK
            )
        ),
        "active_weapon_skin": pa.Column(
            str,
            description="Active weapon skin",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRawValue32,
                scope=Scope.PER_TICK
            )
        ),
        "active_weapon_ammo": pa.Column(
            int,
            description="Active weapon ammo in clip",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iClip1,
                scope=Scope.PER_TICK
            )
        ),
        "total_ammo_left": pa.Column(
            int,
            description="Total reserve ammo",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_pReserveAmmo,
                scope=Scope.PER_TICK
            )
        ),
        "weapon_mode": pa.Column(
            int,
            description="Weapon mode",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_weaponMode,
                scope=Scope.PER_TICK
            )
        ),
        "accuracy_penalty": pa.Column(
            float,
            description="Weapon accuracy penalty",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fAccuracyPenalty,
                scope=Scope.PER_TICK
            )
        ),
        "is_burst_mode": pa.Column(
            bool,
            description="Weapon in burst mode",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bBurstMode,
                scope=Scope.PER_TICK
            )
        ),
        "burst_shots_remaining": pa.Column(
            int,
            description="Burst shots remaining",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iBurstShotsRemaining,
                scope=Scope.PER_TICK
            )
        ),
        "is_in_reload": pa.Column(
            bool,
            description="Weapon is reloading",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInReload,
                scope=Scope.PER_TICK
            )
        ),
        "reload_visually_complete": pa.Column(
            bool,
            description="Reload visually complete",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bReloadVisuallyComplete,
                scope=Scope.PER_TICK
            )
        ),
        "dropped_at_time": pa.Column(
            float,
            description="Time weapon was dropped",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flDroppedAtTime,
                scope=Scope.PER_TICK
            )
        ),
        "looking_at_weapon": pa.Column(
            bool,
            description="Looking at weapon",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsLookingAtWeapon,
                scope=Scope.PER_TICK
            )
        ),
        "holding_look_at_weapon": pa.Column(
            bool,
            description="Holding look at weapon",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsHoldingLookAtWeapon,
                scope=Scope.PER_TICK
            )
        ),
        "is_hauled_back": pa.Column(
            bool,
            description="Weapon is hauled back",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bIsHauledBack,
                scope=Scope.PER_TICK
            )
        ),
        "is_silencer_on": pa.Column(
            bool,
            description="Silencer is on",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bSilencerOn,
                scope=Scope.PER_TICK
            )
        ),
        "time_silencer_switch_complete": pa.Column(
            float,
            description="Time silencer switch complete",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flTimeSilencerSwitchComplete,
                scope=Scope.PER_TICK
            )
        ),
        "last_shot_time": pa.Column(
            float,
            description="Last shot time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_fLastShotTime,
                scope=Scope.PER_TICK
            )
        ),
        "iron_sight_mode": pa.Column(
            int,
            description="Iron sight mode",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iIronSightMode,
                scope=Scope.PER_TICK
            )
        ),
        "num_empty_attacks": pa.Column(
            int,
            description="Number of empty attacks",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iNumEmptyAttacks,
                scope=Scope.PER_TICK
            )
        ),
        "zoom_lvl": pa.Column(
            int,
            description="Zoom level",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_zoomLevel,
                scope=Scope.PER_TICK
            )
        ),
        "needs_bolt_action": pa.Column(
            bool,
            description="Needs bolt action",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bNeedsBoltAction,
                scope=Scope.PER_TICK
            )
        ),
        "next_primary_attack_tick": pa.Column(
            int,
            description="Next primary attack tick",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nNextPrimaryAttackTick,
                scope=Scope.PER_TICK
            )
        ),
        "next_primary_attack_tick_ratio": pa.Column(
            float,
            description="Next primary attack tick ratio",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flNextPrimaryAttackTickRatio,
                scope=Scope.PER_TICK
            )
        ),
        "next_secondary_attack_tick": pa.Column(
            int,
            description="Next secondary attack tick",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nNextSecondaryAttackTick,
                scope=Scope.PER_TICK
            )
        ),
        "next_secondary_attack_tick_ratio": pa.Column(
            float,
            description="Next secondary attack tick ratio",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flNextSecondaryAttackTickRatio,
                scope=Scope.PER_TICK
            )
        ),
        
        # Weapon Ownership & Attributes
        "active_weapon_original_owner": pa.Column(
            str,
            description="Original weapon owner XUID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_OriginalOwnerXuidLow,
                scope=Scope.PER_TICK
            )
        ),
        "item_def_idx": pa.Column(
            int,
            description="Item definition index",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iItemDefinitionIndex,
                scope=Scope.PER_TICK
            )
        ),
        "weapon_quality": pa.Column(
            int,
            description="Weapon quality",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEntityQuality,
                scope=Scope.PER_TICK
            )
        ),
        "entity_lvl": pa.Column(
            int,
            description="Entity level",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iEntityLevel,
                scope=Scope.PER_TICK
            )
        ),
        "item_id_high": pa.Column(
            int,
            description="Item ID high",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iItemIDHigh,
                scope=Scope.PER_TICK
            )
        ),
        "item_id_low": pa.Column(
            int,
            description="Item ID low",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iItemIDLow,
                scope=Scope.PER_TICK
            )
        ),
        "item_account_id": pa.Column(
            int,
            description="Item account ID",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iAccountID,
                scope=Scope.PER_TICK
            )
        ),
        "inventory_position": pa.Column(
            int,
            description="Inventory position",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iInventoryPosition,
                scope=Scope.PER_TICK
            )
        ),
        "is_initialized": pa.Column(
            bool,
            description="Is initialized",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bInitialized,
                scope=Scope.PER_TICK
            )
        ),
        "econ_item_attribute_def_idx": pa.Column(
            int,
            description="Econ item attribute definition index",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iAttributeDefinitionIndex,
                scope=Scope.PER_TICK
            )
        ),
        "initial_value": pa.Column(
            float,
            description="Initial value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flInitialValue,
                scope=Scope.PER_TICK
            )
        ),
        "refundable_currency": pa.Column(
            int,
            description="Refundable currency",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nRefundableCurrency,
                scope=Scope.PER_TICK
            )
        ),
        "set_bonus": pa.Column(
            bool,
            description="Set bonus",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bSetBonus,
                scope=Scope.PER_TICK
            )
        ),
        "custom_name": pa.Column(
            str,
            description="Custom weapon name",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_szCustomName,
                scope=Scope.PER_TICK
            )
        ),
        "orig_owner_xuid_low": pa.Column(
            int,
            description="Original owner XUID low",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_OriginalOwnerXuidLow,
                scope=Scope.PER_TICK
            )
        ),
        "orig_owner_xuid_high": pa.Column(
            int,
            description="Original owner XUID high",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_OriginalOwnerXuidHigh,
                scope=Scope.PER_TICK
            )
        ),
        "fall_back_paint_kit": pa.Column(
            int,
            description="Fallback paint kit",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nFallbackPaintKit,
                scope=Scope.PER_TICK
            )
        ),
        "fall_back_seed": pa.Column(
            int,
            description="Fallback seed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nFallbackSeed,
                scope=Scope.PER_TICK
            )
        ),
        "fall_back_wear": pa.Column(
            float,
            description="Fallback wear",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flFallbackWear,
                scope=Scope.PER_TICK
            )
        ),
        "fall_back_stat_track": pa.Column(
            int,
            description="Fallback stat track",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nFallbackStatTrak,
                scope=Scope.PER_TICK
            )
        ),
        "m_iState": pa.Column(
            int,
            description="Weapon state",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iState,
                scope=Scope.PER_TICK
            )
        ),
        "fire_seq_start_time": pa.Column(
            float,
            description="Fire sequence start time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flFireSequenceStartTime,
                scope=Scope.PER_TICK
            )
        ),
        "fire_seq_start_time_change": pa.Column(
            int,
            description="Fire sequence start time change",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_nFireSequenceStartTimeChange,
                scope=Scope.PER_TICK
            )
        ),
        "is_fire_event_primary": pa.Column(
            bool,
            description="Is fire event primary",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_bPlayerFireEventIsPrimary,
                scope=Scope.PER_TICK
            )
        ),
        "i_recoil_idx": pa.Column(
            int,
            description="Recoil index (int)",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRecoilIndex,
                scope=Scope.PER_TICK
            )
        ),
        "fl_recoil_idx": pa.Column(
            float,
            description="Recoil index (float)",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flRecoilIndex,
                scope=Scope.PER_TICK
            )
        ),
        "post_pone_fire_ready_time": pa.Column(
            float,
            description="Postpone fire ready time",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_flPostponeFireReadyTime,
                scope=Scope.PER_TICK
            )
        ),
        "orig_team_number": pa.Column(
            int,
            description="Original team number",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iOriginalTeamNumber,
                scope=Scope.PER_TICK
            )
        ),
        "prev_owner": pa.Column(
            str,
            description="Previous owner",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_hPrevOwner,
                scope=Scope.PER_TICK
            )
        ),
        "weapon_float": pa.Column(
            float,
            description="Weapon float value",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRawValue32,
                scope=Scope.PER_TICK
            )
        ),
        "weapon_paint_seed": pa.Column(
            int,
            description="Weapon paint seed",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRawValue32,
                scope=Scope.PER_TICK
            )
        ),
        "weapon_stickers": pa.Column(
            str,
            description="Weapon stickers",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.m_iRawValue32,
                scope=Scope.PER_TICK
            )
        ),
        
        # User Command Data (Player Inputs)
        "usercmd_viewangle_x": pa.Column(
            float,
            description="User command view angle X",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_viewangle_y": pa.Column(
            float,
            description="User command view angle Y",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_viewangle_z": pa.Column(
            float,
            description="User command view angle Z",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_buttonstate_1": pa.Column(
            int,
            description="User command button state 1",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_buttonstate_2": pa.Column(
            int,
            description="User command button state 2",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_buttonstate_3": pa.Column(
            int,
            description="User command button state 3",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_consumed_server_angle_changes": pa.Column(
            int,
            description="User command consumed server angle changes",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_forward_move": pa.Column(
            float,
            description="User command forward movement",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_left_move": pa.Column(
            float,
            description="User command left movement",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_impulse": pa.Column(
            int,
            description="User command impulse",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_mouse_dx": pa.Column(
            int,
            description="User command mouse delta X",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_mouse_dy": pa.Column(
            int,
            description="User command mouse delta Y",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_left_hand_desired": pa.Column(
            bool,
            description="User command left hand desired",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_weapon_select": pa.Column(
            int,
            description="User command weapon select",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
        "usercmd_input_history": pa.Column(
            str,
            description="User command input history",
            metadata=MetaStruct(
                ingame_cvar=ServerCVar.NA,
                scope=Scope.PER_TICK,
                ntype=NType.CLIENT
            )
        ),
    },
    strict=False,
    name="demoparser2"
)


class PlayerInfoSchema(pa.DataFrameModel):
    steamid: Series[pa.UInt64] = pa.Field(description="Player's Steam ID")
    name: Series[str] = pa.Field(description="Player's display name") 
    team_number: Series[pa.Int32] = pa.Field(ge=0, le=5, description="Team number (0-5)")
    
    class Config:
        strict = True
        coerce = True

class GrenadeSchema(pa.DataFrameModel):
    grenade_type: Series[str] = pa.Field(description="Type of grenade (e.g., CHEGrenade)")
    grenade_entity_id: Series[pa.Int32] = pa.Field(ge=0, description="Entity ID of the grenade")
    X: Series[float] = pa.Field(nullable=True, description="X coordinate (can be NaN)")
    Y: Series[float] = pa.Field(nullable=True, description="Y coordinate (can be NaN)")
    Z: Series[float] = pa.Field(nullable=True, description="Z coordinate (can be NaN)")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick when event occurred")
    thrower_steamid: Series[pa.UInt64] = pa.Field(description="Player's Steam ID")
    name: Series[str] = pa.Field(description="Player's display name")
    
    class Config:
        strict = True
        coerce = True

class ItemDropSchema(pa.DataFrameModel):
    account_id: Series[pa.Int64] = pa.Field(description="Account ID of the player")
    def_index: Series[pa.Int32] = pa.Field(description="Item definition index")
    dropreason: Series[str] = pa.Field(description="Reason for the item drop")
    inventory: Series[pa.Int32] = pa.Field(description="Inventory slot")
    item_id: Series[pa.Int64] = pa.Field(description="Unique item ID")
    paint_index: Series[pa.Int32] = pa.Field(nullable=True, description="Paint/skin index")
    paint_seed: Series[pa.Int32] = pa.Field(nullable=True, description="Paint seed for pattern")
    paint_wear: Series[pa.Float64] = pa.Field(nullable=True, description="Wear value of the skin")
    custom_name: Series[str] = pa.Field(nullable=True, description="Custom name tag")
    
    class Config:
        strict = True
        coerce = True

class SkinSchema(pa.DataFrameModel):
    def_index: Series[pa.Int32] = pa.Field(description="Item definition index")
    item_id: Series[pa.Int64] = pa.Field(description="Unique item ID")
    paint_index: Series[pa.Int32] = pa.Field(nullable=True, description="Paint/skin index")
    paint_seed: Series[pa.Int32] = pa.Field(nullable=True, description="Paint seed for pattern")
    paint_wear: Series[pa.Float64] = pa.Field(nullable=True, description="Wear value of the skin")
    custom_name: Series[str] = pa.Field(nullable=True, description="Custom name tag")
    steamid: Series[pa.UInt64] = pa.Field(description="Player's Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventItemEquipSchema(pa.DataFrameModel):
    canzoom: Series[bool] = pa.Field(description="Whether weapon can zoom")
    defindex: Series[pa.Int32] = pa.Field(description="Item definition index")
    hassilencer: Series[bool] = pa.Field(description="Whether weapon has silencer")
    hastracers: Series[bool] = pa.Field(description="Whether weapon has tracers")
    ispainted: Series[bool] = pa.Field(description="Whether weapon is painted/skinned")
    issilenced: Series[bool] = pa.Field(description="Whether weapon is currently silenced")
    item: Series[str] = pa.Field(description="Item name")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    weptype: Series[pa.Int32] = pa.Field(description="Weapon type")
    
    class Config:
        strict = True
        coerce = True

class EventWeaponFireSchema(pa.DataFrameModel):
    silenced: Series[bool] = pa.Field(description="Whether shot was silenced")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    weapon: Series[str] = pa.Field(description="Weapon name")
    
    class Config:
        strict = True
        coerce = True

class EventItemPickupSchema(pa.DataFrameModel):
    defindex: Series[pa.Int32] = pa.Field(description="Item definition index")
    item: Series[str] = pa.Field(description="Item name")
    silent: Series[bool] = pa.Field(description="Whether pickup was silent")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerJumpSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerFootstepSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerHurtSchema(pa.DataFrameModel):
    armor: Series[pa.Int32] = pa.Field(ge=0, description="Player armor after damage")
    attacker_name: Series[str] = pa.Field(nullable=True, description="Attacker name")
    attacker_steamid: Series[str] = pa.Field(nullable=True, description="Attacker Steam ID")
    dmg_armor: Series[pa.Int32] = pa.Field(ge=0, description="Damage to armor")
    dmg_health: Series[pa.Int32] = pa.Field(ge=0, description="Damage to health")
    health: Series[pa.Int32] = pa.Field(ge=0, description="Player health after damage")
    hitgroup: Series[str] = pa.Field(description="Body part hit")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Victim name")
    user_steamid: Series[str] = pa.Field(description="Victim Steam ID")
    weapon: Series[str] = pa.Field(description="Weapon used")
    
    class Config:
        strict = True
        coerce = True

class EventHltvChaseSchema(pa.DataFrameModel):
    distance: Series[pa.Int32] = pa.Field(description="Camera distance")
    inertia: Series[pa.Int32] = pa.Field(description="Camera inertia")
    ineye: Series[pa.Int32] = pa.Field(description="In eye view mode")
    phi: Series[pa.Int32] = pa.Field(description="Phi angle")
    target1: Series[pa.Int32] = pa.Field(description="Primary target")
    target2: Series[pa.Int32] = pa.Field(description="Secondary target")
    theta: Series[pa.Int32] = pa.Field(description="Theta angle")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    
    class Config:
        strict = True
        coerce = True

class EventWeaponReloadSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventWeaponZoomSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerSpawnSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventOtherDeathSchema(pa.DataFrameModel):
    attacker_name: Series[str] = pa.Field(nullable=True, description="Attacker name")
    attacker_steamid: Series[str] = pa.Field(nullable=True, description="Attacker Steam ID")
    attackerblind: Series[bool] = pa.Field(description="Whether attacker was blind")
    headshot: Series[bool] = pa.Field(description="Whether it was a headshot")
    noscope: Series[bool] = pa.Field(description="Whether it was a no-scope shot")
    otherid: Series[pa.Int32] = pa.Field(description="Other entity ID")
    othertype: Series[str] = pa.Field(description="Type of other entity")
    penetrated: Series[pa.Int32] = pa.Field(description="Number of walls penetrated")
    thrusmoke: Series[bool] = pa.Field(description="Whether shot was through smoke")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    weapon: Series[str] = pa.Field(description="Weapon used")
    weapon_fauxitemid: Series[str] = pa.Field(nullable=True, description="Weapon faux item ID")
    weapon_itemid: Series[str] = pa.Field(nullable=True, description="Weapon item ID")
    weapon_originalowner_xuid: Series[str] = pa.Field(nullable=True, description="Original weapon owner XUID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerDeathSchema(pa.DataFrameModel):
    assistedflash: Series[bool] = pa.Field(description="Whether kill was assisted by flash")
    assister_name: Series[str] = pa.Field(nullable=True, description="Assister name")
    assister_steamid: Series[str] = pa.Field(nullable=True, description="Assister Steam ID")
    attacker_name: Series[str] = pa.Field(nullable=True, description="Attacker name")
    attacker_steamid: Series[str] = pa.Field(nullable=True, description="Attacker Steam ID")
    attackerblind: Series[bool] = pa.Field(description="Whether attacker was blind")
    attackerinair: Series[bool] = pa.Field(description="Whether attacker was in air")
    distance: Series[pa.Float32] = pa.Field(description="Distance of kill")
    dmg_armor: Series[pa.Int32] = pa.Field(ge=0, description="Damage to armor")
    dmg_health: Series[pa.Int32] = pa.Field(ge=0, description="Damage to health")
    dominated: Series[pa.Int32] = pa.Field(description="Domination status")
    headshot: Series[bool] = pa.Field(description="Whether it was a headshot")
    hitgroup: Series[str] = pa.Field(description="Body part hit")
    noreplay: Series[bool] = pa.Field(description="Whether replay is disabled")
    noscope: Series[bool] = pa.Field(description="Whether it was a no-scope shot")
    penetrated: Series[pa.Int32] = pa.Field(description="Number of walls penetrated")
    revenge: Series[pa.Int32] = pa.Field(description="Revenge kill status")
    thrusmoke: Series[bool] = pa.Field(description="Whether shot was through smoke")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Victim name")
    user_steamid: Series[str] = pa.Field(description="Victim Steam ID")
    weapon: Series[str] = pa.Field(description="Weapon used")
    weapon_fauxitemid: Series[str] = pa.Field(nullable=True, description="Weapon faux item ID")
    weapon_itemid: Series[str] = pa.Field(nullable=True, description="Weapon item ID")
    weapon_originalowner_xuid: Series[str] = pa.Field(nullable=True, description="Original weapon owner XUID")
    wipe: Series[pa.Int32] = pa.Field(description="Team wipe status")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerBlindSchema(pa.DataFrameModel):
    attacker_name: Series[str] = pa.Field(nullable=True, description="Flashbang thrower name")
    attacker_steamid: Series[str] = pa.Field(nullable=True, description="Flashbang thrower Steam ID")
    blind_duration: Series[pa.Float32] = pa.Field(description="Duration of blindness")
    entityid: Series[pa.Int32] = pa.Field(description="Flashbang entity ID")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Blinded player name")
    user_steamid: Series[str] = pa.Field(description="Blinded player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventGrenadeDetonateSchema(pa.DataFrameModel):
    entityid: Series[pa.Int32] = pa.Field(description="Grenade entity ID")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Thrower name")
    user_steamid: Series[str] = pa.Field(description="Thrower Steam ID")
    x: Series[pa.Float32] = pa.Field(description="X coordinate")
    y: Series[pa.Float32] = pa.Field(description="Y coordinate")
    z: Series[pa.Float32] = pa.Field(description="Z coordinate")
    
    class Config:
        strict = True
        coerce = True

class EventHltvFixedSchema(pa.DataFrameModel):
    fov: Series[pa.Float32] = pa.Field(description="Field of view")
    offset: Series[pa.Int32] = pa.Field(description="Camera offset")
    phi: Series[pa.Int32] = pa.Field(description="Phi angle")
    posx: Series[pa.Int32] = pa.Field(description="X position")
    posy: Series[pa.Int32] = pa.Field(description="Y position")
    posz: Series[pa.Int32] = pa.Field(description="Z position")
    target: Series[pa.Int32] = pa.Field(description="Camera target")
    theta: Series[pa.Int32] = pa.Field(description="Theta angle")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    
    class Config:
        strict = True
        coerce = True

class EventServerCvarSchema(pa.DataFrameModel):
    name: Series[str] = pa.Field(description="CVar name")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    value: Series[str] = pa.Field(description="CVar value")
    
    class Config:
        strict = True
        coerce = True

class EventBombPickupSchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventBombDroppedSchema(pa.DataFrameModel):
    entindex: Series[pa.Int32] = pa.Field(description="Bomb entity index")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventServerMessageSchema(pa.DataFrameModel):
    server_message: Series[str] = pa.Field(description="Server message content")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    
    class Config:
        strict = True
        coerce = True

class EventChatMessageSchema(pa.DataFrameModel):
    chat_message: Series[str] = pa.Field(description="Chat message content")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerTeamSchema(pa.DataFrameModel):
    disconnect: Series[bool] = pa.Field(description="Whether player is disconnecting")
    isbot: Series[bool] = pa.Field(description="Whether player is a bot")
    oldteam: Series[pa.Int32] = pa.Field(description="Previous team number")
    silent: Series[bool] = pa.Field(description="Whether team change is silent")
    team: Series[pa.Int32] = pa.Field(description="New team number")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventPlayerDisconnectSchema(pa.DataFrameModel):
    PlayerID: Series[pa.Int32] = pa.Field(description="Player ID")
    name: Series[str] = pa.Field(description="Player name")
    networkid: Series[str] = pa.Field(description="Network ID")
    reason: Series[pa.Int32] = pa.Field(description="Disconnect reason code")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    xuid: Series[pa.UInt64] = pa.Field(description="Player XUID")
    
    class Config:
        strict = True
        coerce = True

class EventBombEventSchema(pa.DataFrameModel):
    site: Series[pa.Int32] = pa.Field(description="Bomb site (A=0, B=1)")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventBombBeginDefuseSchema(pa.DataFrameModel):
    haskit: Series[bool] = pa.Field(description="Whether player has defuse kit")
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    user_name: Series[str] = pa.Field(description="Player name")
    user_steamid: Series[str] = pa.Field(description="Player Steam ID")
    
    class Config:
        strict = True
        coerce = True

class EventTickOnlySchema(pa.DataFrameModel):
    tick: Series[pa.Int32] = pa.Field(ge=0, description="Game tick")
    
    class Config:
        strict = True
        coerce = True