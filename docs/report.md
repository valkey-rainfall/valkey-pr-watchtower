# Valkey PR Health Report

**Generated:** 2026-07-26 08:24 UTC | **Repo:** [valkey-io/valkey](https://github.com/valkey-io/valkey)

_PRs are sorted into lanes by who owns the next move, most immediately actionable first._

---

## 📊 By the Numbers

| Lane | Count |
|------|-------|
| Total open PRs | 308 |
| 🟢 Land-ready | 10 |
| 🤖 Bot / backport | 4 |
| 👀 Ball in reviewer's court | 53 |
| 🗳 Needs a decision | 36 |
| 🏷 Flagged to close | 3 |
| ✍️ Ball in author's court | 177 |
| 📝 Draft (excluded) | 25 |


## 🟢 Land-ready — one click to merge

_Community-approved / to-be-merged, CI not failing, no conflicts._

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [685](https://github.com/valkey-io/valkey/pull/685) | Align the entry read and lag rules of the consumer group | artikell | 2.1y |
| [2972](https://github.com/valkey-io/valkey/pull/2972) | Add an optional parameter to SISMEMBER; return -1 if the key does not… | li-benson | 7mo |
| [3253](https://github.com/valkey-io/valkey/pull/3253) | Add NX,XX,EX,PX support to INCR, INCRBY, INCRBYFLOAT, DECR, DECRBY com… | GavinDmello | 5mo |
| [3465](https://github.com/valkey-io/valkey/pull/3465) | fix: update maxmemory test to account for SDS pre-allocation memory | djk1027 | 3mo |
| [3466](https://github.com/valkey-io/valkey/pull/3466) | XACKDEL Command | nickiaq | 3mo |
| [3467](https://github.com/valkey-io/valkey/pull/3467) | XDELEX Command | nickiaq | 3mo |
| [3491](https://github.com/valkey-io/valkey/pull/3491) | zset: add in-place fast path for score updates in listpack encoding | charsyam | 3mo |
| [3522](https://github.com/valkey-io/valkey/pull/3522) | Fail fast on empty CA directory at TLS config load | yang-z-o | 3mo |
| [3810](https://github.com/valkey-io/valkey/pull/3810) | Fix zrangebyscore empty exclusive bound | chenshi5012 | 2mo |
| [4102](https://github.com/valkey-io/valkey/pull/4102) | Deflake "Replica output bytes metric" with atomic stats capture | Taeknology | 2w |


## 🤖 Bot / backport quick-wins

_Human-approved, fast to land._

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [4225](https://github.com/valkey-io/valkey/pull/4225) | [backport] Backport sweep for 9.1 | valkeyrie-ops[bot] | 5d |
| [4226](https://github.com/valkey-io/valkey/pull/4226) | [backport] Backport sweep for 9.0 | valkeyrie-ops[bot] | 5d |
| [4249](https://github.com/valkey-io/valkey/pull/4249) | [backport] Backport sweep for 8.1 | valkeyrie-ops[bot] | 4d |
| [4250](https://github.com/valkey-io/valkey/pull/4250) | [backport] Backport sweep for 8.0 | valkeyrie-ops[bot] | 4d |


## 🌱 First-Time Contributors

_A timely response may retain a future regular. Cross-cut; each also appears in its lane._

| PR | Title | Author | Age | Lane |
|----|-------|--------|-----|------|
| [4270](https://github.com/valkey-io/valkey/pull/4270) | make getMonotonicUs static in libvalkeylua | mohammedgqudah | 0d | `author_court` |
| [4267](https://github.com/valkey-io/valkey/pull/4267) | Log EXEC in commandlog | michellee-10 | 1d | `reviewer_court` |
| [4257](https://github.com/valkey-io/valkey/pull/4257) | perf: combined post-command pending-work gate in afterCommand() | ahmetalicc | 3d | `reviewer_court` |
| [4254](https://github.com/valkey-io/valkey/pull/4254) | Convert oversized hash listpacks during RDB load | ANSHUL-REAL | 4d | `author_court` |
| [4252](https://github.com/valkey-io/valkey/pull/4252) | valkey-benchmark: fix -r option to support keyspace values above INT_M… | michellee-10 | 4d | `reviewer_court` |
| [4232](https://github.com/valkey-io/valkey/pull/4232) | Bump minimum cmake version to 3.24 | Baraa-Hasheesh | 4d | `author_court` |
| [4216](https://github.com/valkey-io/valkey/pull/4216) | Support Valkey 9.1 rollback compatibility with Redis 6.0 | chenys | 6d | `reviewer_court` |
| [4215](https://github.com/valkey-io/valkey/pull/4215) | valkey-benchmark: reject empty command sequence instead of hanging | dhruv2x | 6d | `author_court` |
| [4214](https://github.com/valkey-io/valkey/pull/4214) | fix(acl): prevent NULL pointer dereference on malformed selector in AC… | magic-peach | 6d | `author_court` |
| [4213](https://github.com/valkey-io/valkey/pull/4213) | fix(debug): add bounds check in memtest_test_linux_anonymous_maps to p… | magic-peach | 6d | `author_court` |
| [4190](https://github.com/valkey-io/valkey/pull/4190) | Reclaim dead client IDs from the tracking table (#4143) | rayjinghaolei | 10d | `author_court` |
| [4176](https://github.com/valkey-io/valkey/pull/4176) | Isolate I/O thread written client fields on a dedicated cache line | abokhalill | 10d | `reviewer_court` |
| [4163](https://github.com/valkey-io/valkey/pull/4163) | Solution (#4143): [BUG] Tracking table items not cleaned after client … | TFGSUMIT | 11d | `author_court` |
| [4160](https://github.com/valkey-io/valkey/pull/4160) | Fix out-of-memory DoS on HRANDFIELD, ZRANDMEMBER and SRANDMEMBER with … | warrenzhu25 | 12d | `author_court` |
| [4159](https://github.com/valkey-io/valkey/pull/4159) | Add configurable auth options for CLUSTER MIGRATESLOTS (#2392) | warrenzhu25 | 12d | `reviewer_court` |
| [4152](https://github.com/valkey-io/valkey/pull/4152) | Account for deferred client frees during eviction | dhruv2x | 13d | `reviewer_court` |
| [4147](https://github.com/valkey-io/valkey/pull/4147) | fix: remove duplicated words and correct grammar in comments | magic-peach | 2w | `author_court` |
| [4146](https://github.com/valkey-io/valkey/pull/4146) | Fix XSETID ENTRIESADDED error message to include the accepted value 0 | nikolauspschuetz | 2w | `author_court` |
| [4145](https://github.com/valkey-io/valkey/pull/4145) | Fix ENTRIESREAD error message to include the accepted value 0 | nikolauspschuetz | 2w | `reviewer_court` |
| [4129](https://github.com/valkey-io/valkey/pull/4129) | Fix out-of-bounds read in vsnprintf_async_signal_safe on a trailing '%… | magic-peach | 2w | `author_court` |
| [4122](https://github.com/valkey-io/valkey/pull/4122) | Fixes RESP response splitting in the Lua shebang error path. | localhost-detect | 2w | `author_court` |
| [4110](https://github.com/valkey-io/valkey/pull/4110) | Remove per-iteration overhead from the IO thread main loop | omerrubi-amzn | 2w | `author_court` |
| [4109](https://github.com/valkey-io/valkey/pull/4109) | Coalesce small bulk replies into a single buffer append | omerrubi-amzn | 2w | `author_court` |
| [4108](https://github.com/valkey-io/valkey/pull/4108) | Skip commandlog bookkeeping when no threshold is crossed | omerrubi-amzn | 2w | `author_court` |
| [4107](https://github.com/valkey-io/valkey/pull/4107) | Fix false sharing in per-thread memory usage counters | omerrubi-amzn | 2w | `author_court` |
| [4106](https://github.com/valkey-io/valkey/pull/4106) | Handle previously unchecked pthread_mutex_* and fclose return values  … | SuchitraShankar07 | 2w | `reviewer_court` |
| [4085](https://github.com/valkey-io/valkey/pull/4085) | sentinel: add state-config-file to separate runtime state from static … | stanhu | 3w | `reviewer_court` |
| [4079](https://github.com/valkey-io/valkey/pull/4079) | Route INFO generation (core + module API) through a pluggable info emi… | omerrubi-amzn | 3w | `author_court` |
| [4050](https://github.com/valkey-io/valkey/pull/4050) | module: add CreateString ReferenceFromKey/Uninitialized, and StringSet… | kvcache | 4w | `reviewer_court` |
| [4010](https://github.com/valkey-io/valkey/pull/4010) | Limit multibulk args count and fix integer type truncations | wufengwind | 5w | `author_court` |
| [4003](https://github.com/valkey-io/valkey/pull/4003) | Add futex-based blocking when main thread waits for IO poll results | asafpamzn | 5w | `author_court` |
| [3976](https://github.com/valkey-io/valkey/pull/3976) | Fix reserved identifier violations in include guards (#3850) | vansvan17 | 6w | `author_court` |
| [3974](https://github.com/valkey-io/valkey/pull/3974) | Fix unbalanced ']' in bitops (BITFIELD_RO) command | ShubhamTaple | 6w | `reviewer_court` |
| [3973](https://github.com/valkey-io/valkey/pull/3973) | Clear import-source flag on connection state reset | tjade273 | 6w | `author_court` |
| [3972](https://github.com/valkey-io/valkey/pull/3972) | Validate PUBLISH and MODULE payload lengths against packet size | tjade273 | 6w | `author_court` |
| [3971](https://github.com/valkey-io/valkey/pull/3971) | Fix GEORADIUS STORE ACL bypass via duplicate options | tjade273 | 6w | `author_court` |
| [3936](https://github.com/valkey-io/valkey/pull/3936) | Add trusted connection pool for admin access (#3918) | vansvan17 | 6w | `reviewer_court` |
| [3906](https://github.com/valkey-io/valkey/pull/3906) | fix: improve Makefile robustness by accomodating file paths with space… | mebinthattil | 7w | `author_court` |
| [3845](https://github.com/valkey-io/valkey/pull/3845) | [BUG] Fix CROSSSLOT error in rebalance when --user is specified withou… | 2030XiaoGe | 8w | `reviewer_court` |
| [3730](https://github.com/valkey-io/valkey/pull/3730) | conf: document chown(2) requirement for unixsocketgroup | moko-poi | 2mo | `author_court` |
| [3729](https://github.com/valkey-io/valkey/pull/3729) | Fix article/grammar errors in code comments | moko-poi | 2mo | `author_court` |
| [3728](https://github.com/valkey-io/valkey/pull/3728) | Fix grammatical typo "This functions" in code comments | moko-poi | 2mo | `author_court` |
| [3705](https://github.com/valkey-io/valkey/pull/3705) | fix: duplicated words in networking/server/function_lua comments | vip892766gma | 2mo | `author_court` |
| [3655](https://github.com/valkey-io/valkey/pull/3655) | MONITOR TRACE: key-level access tracing with sampling | xdk-amz | 2mo | `reviewer_court` |
| [3651](https://github.com/valkey-io/valkey/pull/3651) | info: add command breakdown to Errorstats | servusdei2018 | 2mo | `author_court` |
| [3605](https://github.com/valkey-io/valkey/pull/3605) | Add SIMD (AVX2 + NEON) acceleration for BITOP AND/OR/XOR/NOT | ihabwahbi | 2mo | `author_court` |
| [3603](https://github.com/valkey-io/valkey/pull/3603) | Fix: connSocketBlockingConnect ignores aeWait errors (-1) | xdk-amz | 2mo | `author_court` |
| [3565](https://github.com/valkey-io/valkey/pull/3565) | Implement AOF data integrity check support. | sumitk163 | 3mo | `reviewer_court` |
| [3538](https://github.com/valkey-io/valkey/pull/3538) | Add AUTH/AUTH2 options to CLUSTER MIGRATESLOTS | nemtsv | 3mo | `needs_decision` |
| [3529](https://github.com/valkey-io/valkey/pull/3529) | Add systemd socket activation support | drizzt | 3mo | `reviewer_court` |
| [3467](https://github.com/valkey-io/valkey/pull/3467) | XDELEX Command | nickiaq | 3mo | `land_ready` |
| [3466](https://github.com/valkey-io/valkey/pull/3466) | XACKDEL Command | nickiaq | 3mo | `land_ready` |
| [3427](https://github.com/valkey-io/valkey/pull/3427) | Windows native builds & tests (Microsoft Visual Studio 2026) | SamuelMarks | 3mo | `flagged_close` |
| [3410](https://github.com/valkey-io/valkey/pull/3410) | listpack: add lpFindInteger() to avoid string conversion in set integ… | liveprasad | 4mo | `reviewer_court` |
| [3364](https://github.com/valkey-io/valkey/pull/3364) | Disable original gossip and auto failover logic. Manage the cluster in… | greatsharp | 4mo | `reviewer_court` |
| [3269](https://github.com/valkey-io/valkey/pull/3269) | Convert LTTng tracepoints from duration to entry/exit pairs | MatthewKhouzam | 4mo | `author_court` |
| [3268](https://github.com/valkey-io/valkey/pull/3268) | ci: add top-level permissions to remaining workflows | u-wlkjyy | 4mo | `author_court` |
| [3253](https://github.com/valkey-io/valkey/pull/3253) | Add NX,XX,EX,PX support to INCR, INCRBY, INCRBYFLOAT, DECR, DECRBY com… | GavinDmello | 5mo | `land_ready` |
| [3210](https://github.com/valkey-io/valkey/pull/3210) | tests: make test_entryUpdate allocator-agnostic | seonghoj-bright | 5mo | `author_court` |
| [3207](https://github.com/valkey-io/valkey/pull/3207) | Move CONFIG REWRITE disk I/O to background thread | riskywindow | 5mo | `author_court` |
| [3148](https://github.com/valkey-io/valkey/pull/3148) | fix(cluster): Resolve serverAssert(link != sender->link) crash in larg… | liwei330249526 | 5mo | `author_court` |
| [2982](https://github.com/valkey-io/valkey/pull/2982) | Add option in valkey-benchmark.c to output result in the file | fluorescentury | 7mo | `author_court` |
| [2664](https://github.com/valkey-io/valkey/pull/2664) | add_memalign_func | luorong1999 | 9mo | `author_court` |
| [2331](https://github.com/valkey-io/valkey/pull/2331) | Adding support for DumpSerializedValue API | cdorantes05 | 1.0y | `needs_decision` |
| [2221](https://github.com/valkey-io/valkey/pull/2221) | fix: incomplete printing of the buffer content when a protocol error o… | wstar05 | 1.1y | `reviewer_court` |
| [2213](https://github.com/valkey-io/valkey/pull/2213) | Optimize bitcount by using AVX-512 intrinsic | shanwan1 | 1.1y | `author_court` |
| [1909](https://github.com/valkey-io/valkey/pull/1909) | Add cluster-non-random-gosip option | VyacheslavVanin | 1.3y | `author_court` |
| [1689](https://github.com/valkey-io/valkey/pull/1689) | Implementation of CPU throttling | lschmidtcavalcante-sc | 1.5y | `author_court` |
| [1672](https://github.com/valkey-io/valkey/pull/1672) | Implementation of write throttling | lschmidtcavalcante-sc | 1.5y | `needs_decision` |
| [1547](https://github.com/valkey-io/valkey/pull/1547) | feat: stats and keyspace notifications about lazy expiration | proost | 1.5y | `author_court` |
| [1455](https://github.com/valkey-io/valkey/pull/1455) | Add GETPXT, MGETPXT (Get with millisecond expiration) commands | arcivanov | 1.6y | `needs_decision` |
| [1284](https://github.com/valkey-io/valkey/pull/1284) | fix: readonly client moved inconsistency | proost | 1.7y | `author_court` |
| [568](https://github.com/valkey-io/valkey/pull/568) | Persistence - Remove Unowned Keys | singku | 2.2y | `author_court` |


## 👀 Ball in Reviewer's Court

_Author acted last — these need a reviewer. Longest-waiting first._

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [2221](https://github.com/valkey-io/valkey/pull/2221) | fix: incomplete printing of the buffer content when a protocol error o… | wstar05 | 1.1y |
| [2011](https://github.com/valkey-io/valkey/pull/2011) | Log failed cluster node(s) state periodically to capture transient sta… | hpatro | 1.2y |
| [2575](https://github.com/valkey-io/valkey/pull/2575) | valkey-benchmark: Tests for ZSCORE, ZRANGE and SISMEMBER | ranshid | 10mo |
| [1781](https://github.com/valkey-io/valkey/pull/1781) | standalone REDIRECT: Fix scripting and further MULTI/EXEC scenarios | gmbnomis | 1.4y |
| [2933](https://github.com/valkey-io/valkey/pull/2933) | Don't require node-id to be null terminated in VM_GetClusterNodeInfo | deepakrn | 7mo |
| [3114](https://github.com/valkey-io/valkey/pull/3114) | latency doctor: report last seen timestamp for latency events | YiwenZhang12 | 6mo |
| [2307](https://github.com/valkey-io/valkey/pull/2307) | [optimization] Optimization of Sentinel Configuration File Update Stra… | youngmore1024 | 1.1y |
| [3529](https://github.com/valkey-io/valkey/pull/3529) | Add systemd socket activation support | drizzt | 3mo |
| [3049](https://github.com/valkey-io/valkey/pull/3049) | Fix flaky test in manual-failover.tcl | Nikhil-Manglore | 6mo |
| [3410](https://github.com/valkey-io/valkey/pull/3410) | listpack: add lpFindInteger() to avoid string conversion in set integ… | liveprasad | 4mo |
| [3496](https://github.com/valkey-io/valkey/pull/3496) | aof: write directly to server.aof_buf in feedAppendOnlyFile | charsyam | 3mo |
| [3739](https://github.com/valkey-io/valkey/pull/3739) | Makefile Fix: LTO flags silently dropped when OPTIMIZATION is set on c… | rainsupreme | 2mo |
| [3706](https://github.com/valkey-io/valkey/pull/3706) | Migrate evalCtx.scripts from dict to hashtable, saving 64B per item an… | rainsupreme | 2mo |
| [3893](https://github.com/valkey-io/valkey/pull/3893) | Add repl-disable-full-resync-until to gate primary full resync | artikell | 7w |
| [3845](https://github.com/valkey-io/valkey/pull/3845) | [BUG] Fix CROSSSLOT error in rebalance when --user is specified withou… | 2030XiaoGe | 8w |
| [3974](https://github.com/valkey-io/valkey/pull/3974) | Fix unbalanced ']' in bitops (BITFIELD_RO) command | ShubhamTaple | 6w |
| [3709](https://github.com/valkey-io/valkey/pull/3709) | feat: Add valkey-check-acl offline ACL file validator | yulazariy | 2mo |
| [3364](https://github.com/valkey-io/valkey/pull/3364) | Disable original gossip and auto failover logic. Manage the cluster in… | greatsharp | 4mo |
| [3966](https://github.com/valkey-io/valkey/pull/3966) | Add per-slot memory-bytes metric to CLUSTER SLOT-STATS | eifrah-aws | 6w |
| [3645](https://github.com/valkey-io/valkey/pull/3645) | fix: Reject module writes during client pause to prevent crash | smkher | 2mo |
| [3724](https://github.com/valkey-io/valkey/pull/3724) | Add sync-from-replica with delayed primary switch | avifenesh | 2mo |
| [4085](https://github.com/valkey-io/valkey/pull/4085) | sentinel: add state-config-file to separate runtime state from static … | stanhu | 3w |
| [4106](https://github.com/valkey-io/valkey/pull/4106) | Handle previously unchecked pthread_mutex_* and fclose return values  … | SuchitraShankar07 | 2w |
| [4091](https://github.com/valkey-io/valkey/pull/4091) | Fix crash when processing heartbeat from a node with no local role | enjoy-binbin | 3w |
| [4119](https://github.com/valkey-io/valkey/pull/4119) | Fix NULL pointer arithmetic in scripting engine's wrapText() | xiejing-dev | 2w |
| [4145](https://github.com/valkey-io/valkey/pull/4145) | Fix ENTRIESREAD error message to include the accepted value 0 | nikolauspschuetz | 2w |
| [3936](https://github.com/valkey-io/valkey/pull/3936) | Add trusted connection pool for admin access (#3918) | vansvan17 | 6w |
| [3807](https://github.com/valkey-io/valkey/pull/3807) | GEOSEARCH BYPATH — search along a route/corridor | sushilpaneru1 | 2mo |
| [4159](https://github.com/valkey-io/valkey/pull/4159) | Add configurable auth options for CLUSTER MIGRATESLOTS (#2392) | warrenzhu25 | 12d |
| [3655](https://github.com/valkey-io/valkey/pull/3655) | MONITOR TRACE: key-level access tracing with sampling | xdk-amz | 2mo |
| [4152](https://github.com/valkey-io/valkey/pull/4152) | Account for deferred client frees during eviction | dhruv2x | 13d |
| [4176](https://github.com/valkey-io/valkey/pull/4176) | Isolate I/O thread written client fields on a dedicated cache line | abokhalill | 10d |
| [4124](https://github.com/valkey-io/valkey/pull/4124) | Wait past the HEXPIREAT deadline in the non-existing fields negative t… | AlisinaDevelo | 2w |
| [4090](https://github.com/valkey-io/valkey/pull/4090) | Prevent forgotten nodes from rejoining the cluster via MEET | AlisinaDevelo | 3w |
| [3985](https://github.com/valkey-io/valkey/pull/3985) | Fix LSET listpack conversion after element replacement | Taeknology | 5w |
| [3967](https://github.com/valkey-io/valkey/pull/3967) | Add ACL role support | yang-z-o | 6w |
| [3708](https://github.com/valkey-io/valkey/pull/3708) | Add server-side hot key detection | alon-arenberg | 2mo |
| [4253](https://github.com/valkey-io/valkey/pull/4253) | Fix RESP3 push frame torn apart on self-publish with copy avoidance | quanyeyang | 4d |
| [4223](https://github.com/valkey-io/valkey/pull/4223) | Deflake ccov: Contain slot migration test failures with a recovery bar… | rainsupreme | 5d |
| [4216](https://github.com/valkey-io/valkey/pull/4216) | Support Valkey 9.1 rollback compatibility with Redis 6.0 | chenys | 6d |
| [4212](https://github.com/valkey-io/valkey/pull/4212) | Fix/ready key blocked client uaf 4198 | quanyeyang | 7d |
| [4191](https://github.com/valkey-io/valkey/pull/4191) | Added changes to propogate FLUSHSLOT instead of UNLINK in replication … | omanges | 9d |
| [3565](https://github.com/valkey-io/valkey/pull/3565) | Implement AOF data integrity check support. | sumitk163 | 3mo |
| [3118](https://github.com/valkey-io/valkey/pull/3118) | Incr the dirty counter when deleting expired keys/fields from active e… | enjoy-binbin | 5mo |
| [4259](https://github.com/valkey-io/valkey/pull/4259) | Support dual-channel atomic slot migration | murphyjacob4 | 3d |
| [4080](https://github.com/valkey-io/valkey/pull/4080) | Make serverObject (robj) opaque | rainsupreme | 3w |
| [4050](https://github.com/valkey-io/valkey/pull/4050) | module: add CreateString ReferenceFromKey/Uninitialized, and StringSet… | kvcache | 4w |
| [3531](https://github.com/valkey-io/valkey/pull/3531) | Streaming Compression support for RDB | sarthakaggarwal97 | 3mo |
| [4206](https://github.com/valkey-io/valkey/pull/4206) | ZSET B+ Tree PR 3: Replace skiplist with FB+ Tree implementation | rainsupreme | 8d |
| [4179](https://github.com/valkey-io/valkey/pull/4179) | Deflake: replace flaky wall-clock defrag latency assertion with determ… | rainsupreme | 10d |
| [4267](https://github.com/valkey-io/valkey/pull/4267) | Log EXEC in commandlog | michellee-10 | 1d |
| [4252](https://github.com/valkey-io/valkey/pull/4252) | valkey-benchmark: fix -r option to support keyspace values above INT_M… | michellee-10 | 4d |
| [4257](https://github.com/valkey-io/valkey/pull/4257) | perf: combined post-command pending-work gate in afterCommand() | ahmetalicc | 3d |


## 🗳 Needs a Decision

_Blocked on a community decision._

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [962](https://github.com/valkey-io/valkey/pull/962) | Add command "Client Capa subv2" to change behavior for SUBSCRIBE and S… | hwware | 1.9y |
| [978](https://github.com/valkey-io/valkey/pull/978) | Add last_fork_start_time to INFO STATS | enjoy-binbin | 1.9y |
| [1151](https://github.com/valkey-io/valkey/pull/1151) | Adding KEYINFO command to find out keys that have large number of elem… | otheng03 | 1.8y |
| [1418](https://github.com/valkey-io/valkey/pull/1418) | Add new SCRIPT STATS subcommand | artikell | 1.6y |
| [1455](https://github.com/valkey-io/valkey/pull/1455) | Add GETPXT, MGETPXT (Get with millisecond expiration) commands | arcivanov | 1.6y |
| [1672](https://github.com/valkey-io/valkey/pull/1672) | Implementation of write throttling | lschmidtcavalcante-sc | 1.5y |
| [1964](https://github.com/valkey-io/valkey/pull/1964) | Add sentinel failover SAFE option | li-benson | 1.3y |
| [2157](https://github.com/valkey-io/valkey/pull/2157) | Kill the busy script during failover to avoid data inconsistency | enjoy-binbin | 1.2y |
| [2204](https://github.com/valkey-io/valkey/pull/2204) | Add cluster-replica-priority to allow better ranking in auto failover | enjoy-binbin | 1.1y |
| [2275](https://github.com/valkey-io/valkey/pull/2275) | Add keyspace-hits and keyspace-misses metrics under CLUSTER SLOT-STATS… | enjoy-binbin | 1.1y |
| [2331](https://github.com/valkey-io/valkey/pull/2331) | Adding support for DumpSerializedValue API | cdorantes05 | 1.0y |
| [2368](https://github.com/valkey-io/valkey/pull/2368) | add parameter for initiating bgrewriteaof on exceeding threshold AOF s… | kronwerk | 1.0y |
| [2385](https://github.com/valkey-io/valkey/pull/2385) | Allow dynamic modification of databases num if the db is not been used | enjoy-binbin | 12mo |
| [2586](https://github.com/valkey-io/valkey/pull/2586) | Fix two primaries scenario due to unknown shard_id | deepakrn | 10mo |
| [2689](https://github.com/valkey-io/valkey/pull/2689) | Fix #2678 don't add loadmodule when from config | remicollet | 9mo |
| [2891](https://github.com/valkey-io/valkey/pull/2891) | Reset prefetch and ACL stats via CONFIG RESETSTAT | enjoy-binbin | 7mo |
| [2971](https://github.com/valkey-io/valkey/pull/2971) | Add used_memory_overhead_human and used_memory_dataset_human info fiel… | enjoy-binbin | 7mo |
| [2979](https://github.com/valkey-io/valkey/pull/2979) | Add VM_AddCommandACLCategories API to assign ACL categories to existin… | bandalgomsu | 7mo |
| [2990](https://github.com/valkey-io/valkey/pull/2990) | Avoid loading keys for unowned slots | ranshid | 6mo |
| [3068](https://github.com/valkey-io/valkey/pull/3068) | Cleanup around FAST command flag | enjoy-binbin | 6mo |
| [3191](https://github.com/valkey-io/valkey/pull/3191) | Runtime Payload Histogram Tracking | YiwenZhang12 | 5mo |
| [3212](https://github.com/valkey-io/valkey/pull/3212) | support for tagged metadata in listpack encoding | frostzt | 5mo |
| [3381](https://github.com/valkey-io/valkey/pull/3381) | Write-behind log for async AOF-based durability | jjuleslasarte | 4mo |
| [3409](https://github.com/valkey-io/valkey/pull/3409) | Add AOF rewrite support for module auxiliary data | soloestoy | 4mo |
| [3438](https://github.com/valkey-io/valkey/pull/3438) | Cluster Bus IO offload | hpatro | 3mo |
| [3538](https://github.com/valkey-io/valkey/pull/3538) | Add AUTH/AUTH2 options to CLUSTER MIGRATESLOTS | nemtsv | 3mo |
| [3646](https://github.com/valkey-io/valkey/pull/3646) | Change default of commandlog-reply-larger-than to disable tracking | dvkashapov | 2mo |
| [3911](https://github.com/valkey-io/valkey/pull/3911) | Make VM_CallArgv() API public | dvkashapov | 7w |
| [3986](https://github.com/valkey-io/valkey/pull/3986) | fix: Prevent EXISTS from incrementing keyspace hit/miss stats | yulazariy | 5w |
| [4019](https://github.com/valkey-io/valkey/pull/4019) | Implement `MULTIIF` Command | bandalgomsu | 4w |
| [4128](https://github.com/valkey-io/valkey/pull/4128) | Implement `VM_AllocateExternalMemory` | bandalgomsu | 2w |
| [4148](https://github.com/valkey-io/valkey/pull/4148) | Add CMD_STALE flag to SYNC/PSYNC commands | enjoy-binbin | 2w |
| [4169](https://github.com/valkey-io/valkey/pull/4169) | Add per-direction cluster link established counter info fields | enjoy-binbin | 11d |
| [4197](https://github.com/valkey-io/valkey/pull/4197) | Track full sync completion time | satheeshaGowda | 9d |
| [4230](https://github.com/valkey-io/valkey/pull/4230) | Add DENYOOM flag to SUBSCRIBE, PSUBSCRIBE, SSUBSCRIBE, WATCH | enjoy-binbin | 5d |
| [4268](https://github.com/valkey-io/valkey/pull/4268) | Add script-check-maxmemory to bound memory growth of scripts | enjoy-binbin | 1d |


## 🔥 Deflake / Test-Fix

_Merging these reduces CI noise. Cross-cut; each also appears in its lane._

| PR | Title | Author | Age | Lane |
|----|-------|--------|-----|------|
| [3049](https://github.com/valkey-io/valkey/pull/3049) | Fix flaky test in manual-failover.tcl | Nikhil-Manglore | 6mo | `reviewer_court` |
| [3969](https://github.com/valkey-io/valkey/pull/3969) | Test framework: avoid stale tmpdir reuse on PID collision | zuiderkwast | 6w | `excluded_draft` |
| [4102](https://github.com/valkey-io/valkey/pull/4102) | Deflake "Replica output bytes metric" with atomic stats capture | Taeknology | 2w | `land_ready` |
| [4179](https://github.com/valkey-io/valkey/pull/4179) | Deflake: replace flaky wall-clock defrag latency assertion with determ… | rainsupreme | 10d | `reviewer_court` |
| [4223](https://github.com/valkey-io/valkey/pull/4223) | Deflake ccov: Contain slot migration test failures with a recovery bar… | rainsupreme | 5d | `reviewer_court` |
| [4251](https://github.com/valkey-io/valkey/pull/4251) | deflake ccov: Use _exit() when a child is killed by SIGUSR1 | rainsupreme | 4d | `author_court` |


## 📮 Outreach Dry-Run

_**Dry-run only.** Nothing is posted, closed, or labelled automatically — these are proposals for a human to review and act on._


### Re-engage (reviewer's court, idle ≥60d)

| PR | Title | Author | Evidence | Proposed action |
|----|-------|--------|----------|-----------------|
| [3739](https://github.com/valkey-io/valkey/pull/3739) | Makefile Fix: LTO flags silently dropped when OPTI… | rainsupreme | author acted last; awaiting review; no activity in about 2 months (cooling) | `ping_reengage` |
| [3706](https://github.com/valkey-io/valkey/pull/3706) | Migrate evalCtx.scripts from dict to hashtable, sa… | rainsupreme | author acted last; awaiting review; no activity in about 2 months (cooling) | `ping_reengage` |
| [3529](https://github.com/valkey-io/valkey/pull/3529) | Add systemd socket activation support | drizzt | author acted last; awaiting review; no activity in about 3 months (dormant) | `ping_reengage` |
| [3496](https://github.com/valkey-io/valkey/pull/3496) | aof: write directly to server.aof_buf in feedAppen… | charsyam | author acted last; awaiting review; no activity in about 2 months (cooling) | `ping_reengage` |
| [3410](https://github.com/valkey-io/valkey/pull/3410) | listpack: add lpFindInteger() to avoid string conv… | liveprasad | author acted last; awaiting review; no activity in about 3 months (dormant) | `ping_reengage` |
| [3114](https://github.com/valkey-io/valkey/pull/3114) | latency doctor: report last seen timestamp for lat… | YiwenZhang12 | author acted last; awaiting review; no activity in about 5 months (dormant) | `ping_reengage` |
| [3049](https://github.com/valkey-io/valkey/pull/3049) | Fix flaky test in manual-failover.tcl | Nikhil-Manglore | author acted last; awaiting review; no activity in about 3 months (dormant) | `ping_reengage` |
| [2933](https://github.com/valkey-io/valkey/pull/2933) | Don't require node-id to be null terminated in VM_… | deepakrn | author acted last; awaiting review; no activity in about 6 months (stale) | `ping_reengage` |
| [2575](https://github.com/valkey-io/valkey/pull/2575) | valkey-benchmark: Tests for ZSCORE, ZRANGE and SIS… | ranshid | author acted last; awaiting review; no activity in about 10 months (stale) | `ping_reengage` |
| [2307](https://github.com/valkey-io/valkey/pull/2307) | [optimization] Optimization of Sentinel Configurat… | youngmore1024 | author acted last; awaiting review; no activity in about 5 months (dormant) | `ping_reengage` |
| [2221](https://github.com/valkey-io/valkey/pull/2221) | fix: incomplete printing of the buffer content whe… | wstar05 | author acted last; awaiting review; no activity in over 1 year (ancient) | `ping_reengage` |
| [2011](https://github.com/valkey-io/valkey/pull/2011) | Log failed cluster node(s) state periodically to c… | hpatro | author acted last; awaiting review; no activity in over 1 year (ancient) | `ping_reengage` |
| [1781](https://github.com/valkey-io/valkey/pull/1781) | standalone REDIRECT: Fix scripting and further MUL… | gmbnomis | author acted last; awaiting review; no activity in about 8 months (stale) | `ping_reengage` |


### Closure candidates (author's court, idle ≥90d)

| PR | Title | Author | Evidence | Proposed action |
|----|-------|--------|----------|-----------------|
| [3549](https://github.com/valkey-io/valkey/pull/3549) | tls: prevent stale auto-reload from overriding CON… | charsyam | no activity in about 3 months (dormant) | `comment_and_close` |
| [3508](https://github.com/valkey-io/valkey/pull/3508) | Fix TLS infinite busy loop when write/read handler… | yairgott | CI failing; merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [3490](https://github.com/valkey-io/valkey/pull/3490) | Add LCS LEN fast path using rolling two-row DP | charsyam | CI failing; no activity in about 3 months (dormant) | `comment_and_close` |
| [3480](https://github.com/valkey-io/valkey/pull/3480) | Minor optimizations for CLUSTER SHARDS | nmvk | merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [3428](https://github.com/valkey-io/valkey/pull/3428) | Improve AGENTS.md with comprehensive development g… | soloestoy | merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [3413](https://github.com/valkey-io/valkey/pull/3413) | Optimize infoCommand with SDS pre-allocation | charsyam | CI failing; no activity in about 3 months (dormant) | `comment_and_close` |
| [3383](https://github.com/valkey-io/valkey/pull/3383) | allow to disable dlopen for rdma libs | remicollet | CI failing; no activity in about 4 months (dormant) | `comment_and_close` |
| [3376](https://github.com/valkey-io/valkey/pull/3376) | Fix valkey-benchmark `FUNCTION LOAD` write to repl… | hieu2102 | CI failing; merge conflicts; no activity in about 4 months (dormant) | `comment_and_close` |
| [3348](https://github.com/valkey-io/valkey/pull/3348) | Ignore stale readable callbacks after replica sync… | sarthakaggarwal97 | no activity in about 4 months (dormant) | `comment_and_close` |
| [3305](https://github.com/valkey-io/valkey/pull/3305) | empty kvstore when it has empty allocated hashtabl… | aradz44 | CI failing; no activity in about 4 months (dormant) | `comment_and_close` |
| [3302](https://github.com/valkey-io/valkey/pull/3302) | Fix TSAN compatibility for module loading | baswanth09 | CI failing; no activity in about 4 months (dormant) | `comment_and_close` |
| [3296](https://github.com/valkey-io/valkey/pull/3296) | External data (aka tiered storage?) core with test… | kronwerk | CI failing; merge conflicts; no activity in about 4 months (dormant) | `comment_and_close` |
| [3269](https://github.com/valkey-io/valkey/pull/3269) | Convert LTTng tracepoints from duration to entry/e… | MatthewKhouzam | merge conflicts; changes requested, not addressed; no activity in about 4 months (dormant) | `ping_gentle_nudge` |
| [3268](https://github.com/valkey-io/valkey/pull/3268) | ci: add top-level permissions to remaining workflo… | u-wlkjyy | no activity in about 4 months (dormant) | `ping_gentle_nudge` |
| [3245](https://github.com/valkey-io/valkey/pull/3245) | Fix assertion crash in processIOThreadsReadDone wh… | aradz44 | CI failing; merge conflicts; no activity in about 4 months (dormant) | `comment_and_close` |
| [3239](https://github.com/valkey-io/valkey/pull/3239) | Fix SIGTERM crash during Lua script execution | dvkashapov | no activity in about 5 months (dormant) | `comment_and_close` |
| [3210](https://github.com/valkey-io/valkey/pull/3210) | tests: make test_entryUpdate allocator-agnostic | seonghoj-bright | merge conflicts; no activity in about 4 months (dormant) | `ping_gentle_nudge` |
| [3207](https://github.com/valkey-io/valkey/pull/3207) | Move CONFIG REWRITE disk I/O to background thread | riskywindow | merge conflicts; no activity in about 4 months (dormant) | `ping_gentle_nudge` |
| [3189](https://github.com/valkey-io/valkey/pull/3189) | implement replica-announce-name | bandalgomsu | merge conflicts; no activity in about 5 months (dormant) | `comment_and_close` |
| [3169](https://github.com/valkey-io/valkey/pull/3169) | Support using base aof for full synchronization | cjx-zar | merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [3157](https://github.com/valkey-io/valkey/pull/3157) | Increase valkey-benchmark max latency bucket to 60… | gabiganam | no activity in about 5 months (dormant) | `comment_and_close` |
| [3153](https://github.com/valkey-io/valkey/pull/3153) | add warning log when certs are expired/not yet val… | YiwenZhang12 | merge conflicts; no activity in about 5 months (dormant) | `comment_and_close` |
| [3148](https://github.com/valkey-io/valkey/pull/3148) | fix(cluster): Resolve serverAssert(link != sender-… | liwei330249526 | CI failing; no activity in about 5 months (dormant) | `ping_gentle_nudge` |
| [3105](https://github.com/valkey-io/valkey/pull/3105) | SET: add IFNE conditional option | arshidkv12 | no activity in about 5 months (dormant) | `comment_and_close` |
| [2989](https://github.com/valkey-io/valkey/pull/2989) | Fix empty shard reconfiguration after CLUSTER RESE… | enjoy-binbin | merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [2982](https://github.com/valkey-io/valkey/pull/2982) | Add option in valkey-benchmark.c to output result … | fluorescentury | merge conflicts; no activity in about 4 months (dormant) | `ping_gentle_nudge` |
| [2976](https://github.com/valkey-io/valkey/pull/2976) | Offload read commands cluster mode enabled | uriyage | merge conflicts; no activity in about 4 months (dormant) | `comment_and_close` |
| [2965](https://github.com/valkey-io/valkey/pull/2965) | Hotkey detection function | li-benson | merge conflicts; no activity in about 3 months (dormant) | `comment_and_close` |
| [2914](https://github.com/valkey-io/valkey/pull/2914) | Add TLS client presented certificate expiry warnin… | YiwenZhang12 | merge conflicts; no activity in about 6 months (stale) | `comment_and_close` |
| [2820](https://github.com/valkey-io/valkey/pull/2820) | Implemented a merge queue for PRs | Nikhil-Manglore | merge conflicts; no activity in about 6 months (stale) | `comment_and_close` |
| [2795](https://github.com/valkey-io/valkey/pull/2795) | updated modules examples to compile on Valkey 7.2 … | dmitrypol | CI failing; merge conflicts; no activity in about 8 months (stale) | `comment_and_close` |
| [2664](https://github.com/valkey-io/valkey/pull/2664) | add_memalign_func | luorong1999 | no activity in about 5 months (dormant) | `ping_gentle_nudge` |
| [2627](https://github.com/valkey-io/valkey/pull/2627) | Skip AOF rewrite when a short write occurs | chenyang8094 | CI failing; no activity in about 3 months (dormant) | `comment_and_close` |
| [2577](https://github.com/valkey-io/valkey/pull/2577) | bio.c: Split thread function into smaller parts v2 | TedLyngmo | merge conflicts; no activity in about 10 months (stale) | `comment_and_close` |
| [2576](https://github.com/valkey-io/valkey/pull/2576) | bio.c: Split thread function into smaller parts | TedLyngmo | merge conflicts; no activity in about 10 months (stale) | `comment_and_close` |
| [2552](https://github.com/valkey-io/valkey/pull/2552) | Multi Threaded RDB Load | Nicky-2000 | merge conflicts; no activity in about 10 months (stale) | `comment_and_close` |
| [2551](https://github.com/valkey-io/valkey/pull/2551) | Roll backward downgrade compatibility from Redis 7… | satheeshaGowda | no activity in about 10 months (stale) | `comment_and_close` |
| [2496](https://github.com/valkey-io/valkey/pull/2496) | Add static specifier to the internal functions of … | yzc-yzc | merge conflicts; no activity in about 8 months (stale) | `comment_and_close` |
| [2318](https://github.com/valkey-io/valkey/pull/2318) | change check order for xautoclaim | charsyam | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2306](https://github.com/valkey-io/valkey/pull/2306) | Unexpected variable overriding from .make-settings… | yzc-yzc | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2265](https://github.com/valkey-io/valkey/pull/2265) | Implement tunneling support for non-cluster post-f… | yairgott | merge conflicts; no activity in about 11 months (stale) | `comment_and_close` |
| [2255](https://github.com/valkey-io/valkey/pull/2255) | Accept socket judge fd overflow | kukey | CI failing; no activity in about 7 months (stale) | `comment_and_close` |
| [2253](https://github.com/valkey-io/valkey/pull/2253) | Spelling 17 | jsoref | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `comment_and_close` |
| [2252](https://github.com/valkey-io/valkey/pull/2252) | Spelling 16 | jsoref | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2251](https://github.com/valkey-io/valkey/pull/2251) | spelling: set up | jsoref | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `comment_and_close` |
| [2250](https://github.com/valkey-io/valkey/pull/2250) | Spelling 14 | jsoref | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2249](https://github.com/valkey-io/valkey/pull/2249) | Spelling 13 | jsoref | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `comment_and_close` |
| [2248](https://github.com/valkey-io/valkey/pull/2248) | spelling: otherwise, | jsoref | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2247](https://github.com/valkey-io/valkey/pull/2247) | spelling: nonexistent | jsoref | CI failing; merge conflicts; changes requested, not addressed; no activity in about 11 months (stale) | `comment_and_close` |
| [2244](https://github.com/valkey-io/valkey/pull/2244) | Spelling 7 | jsoref | CI failing; merge conflicts; changes requested, not addressed; no activity in about 11 months (stale) | `comment_and_close` |
| [2243](https://github.com/valkey-io/valkey/pull/2243) | Spelling 6 | jsoref | merge conflicts; no activity in about 11 months (stale) | `comment_and_close` |
| [2242](https://github.com/valkey-io/valkey/pull/2242) | spelling: cannot | jsoref | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2241](https://github.com/valkey-io/valkey/pull/2241) | Spelling 4 | jsoref | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `comment_and_close` |
| [2239](https://github.com/valkey-io/valkey/pull/2239) | Spelling 2 | jsoref | merge conflicts; no activity in about 11 months (stale) | `comment_and_close` |
| [2238](https://github.com/valkey-io/valkey/pull/2238) | spelling: ; otherwise, | jsoref | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [2213](https://github.com/valkey-io/valkey/pull/2213) | Optimize bitcount by using AVX-512 intrinsic | shanwan1 | CI failing; merge conflicts; no activity in about 11 months (stale) | `ping_gentle_nudge` |
| [2183](https://github.com/valkey-io/valkey/pull/2183) | Spelling | jsoref | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `comment_and_close` |
| [1927](https://github.com/valkey-io/valkey/pull/1927) | Mark primary node as alive immediately if reachabl… | hpatro | no activity in over 1 year (ancient) | `comment_and_close` |
| [1909](https://github.com/valkey-io/valkey/pull/1909) | Add cluster-non-random-gosip option | VyacheslavVanin | merge conflicts; no activity in over 1 year (ancient) | `ping_gentle_nudge` |
| [1888](https://github.com/valkey-io/valkey/pull/1888) | Change the usec_per_call operation from float to l… | bluayer | no activity in over 1 year (ancient) | `comment_and_close` |
| [1689](https://github.com/valkey-io/valkey/pull/1689) | Implementation of CPU throttling | lschmidtcavalcante-sc | merge conflicts; no activity in over 1 year (ancient) | `ping_gentle_nudge` |
| [1547](https://github.com/valkey-io/valkey/pull/1547) | feat: stats and keyspace notifications about lazy … | proost | merge conflicts; no activity in over 1 year (ancient) | `ping_gentle_nudge` |
| [1543](https://github.com/valkey-io/valkey/pull/1543) | Use MSG_ZEROCOPY for plaintext replication traffic | murphyjacob4 | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [1424](https://github.com/valkey-io/valkey/pull/1424) | Add latency sample for transaction and pipeline | RayaCoo | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [1407](https://github.com/valkey-io/valkey/pull/1407) | Add tests for src/module examples | Codebells | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [1284](https://github.com/valkey-io/valkey/pull/1284) | fix: readonly client moved inconsistency | proost | merge conflicts; no activity in over 1 year (ancient) | `ping_gentle_nudge` |
| [1120](https://github.com/valkey-io/valkey/pull/1120) | Add admin-port to let administrator connect to the… | hwware | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [1038](https://github.com/valkey-io/valkey/pull/1038) | Add test cases for valkey-benchmark negative path | Shivshankar-Reddy | no activity in over 1 year (ancient) | `comment_and_close` |
| [929](https://github.com/valkey-io/valkey/pull/929) | Remove direct reference to conn->fd and use the co… | naglera | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [906](https://github.com/valkey-io/valkey/pull/906) | Keep the log fd, don't re-open logfile in every lo… | enjoy-binbin | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [866](https://github.com/valkey-io/valkey/pull/866) | New maxmemory-scripts config to limit all cached s… | enjoy-binbin | merge conflicts; no activity in about 4 months (dormant) | `comment_and_close` |
| [831](https://github.com/valkey-io/valkey/pull/831) | Add maxmemory-reserved parameter for evicting key … | hwware | no activity in over 1 year (ancient) | `comment_and_close` |
| [750](https://github.com/valkey-io/valkey/pull/750) | Persist AOF file by io_uring | Wenwen-Chen | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |
| [707](https://github.com/valkey-io/valkey/pull/707) | Allow multi-slot MGET in Cluster Mode | JohnSully | merge conflicts; no activity in about 8 months (stale) | `comment_and_close` |
| [690](https://github.com/valkey-io/valkey/pull/690) | Refactor debug configuration options for clarity a… | PingXie | merge conflicts; no activity in over 2 years (ancient) | `comment_and_close` |
| [663](https://github.com/valkey-io/valkey/pull/663) | Fix 32-bit atomic linking on powerpc | PingXie | no activity in about 11 months (stale) | `comment_and_close` |
| [599](https://github.com/valkey-io/valkey/pull/599) | Use io_uring to make fsync asynchronous when set a… | zhulipeng | merge conflicts; no activity in over 2 years (ancient) | `comment_and_close` |
| [568](https://github.com/valkey-io/valkey/pull/568) | Persistence - Remove Unowned Keys | singku | merge conflicts; changes requested, not addressed; no activity in over 1 year (ancient) | `ping_gentle_nudge` |
| [449](https://github.com/valkey-io/valkey/pull/449) | Batch applying events to kqueue | panjf2000 | merge conflicts; no activity in over 2 years (ancient) | `comment_and_close` |
| [405](https://github.com/valkey-io/valkey/pull/405) | add user-client mapping. | Shuen14 | merge conflicts; changes requested, not addressed; no activity in over 2 years (ancient) | `comment_and_close` |
| [363](https://github.com/valkey-io/valkey/pull/363) | Add support for compiling with mimalloc  | WM0323 | merge conflicts; no activity in over 2 years (ancient) | `comment_and_close` |
| [356](https://github.com/valkey-io/valkey/pull/356) | Background Job Manager (BJM) - replacement for BIO | JimB123 | merge conflicts; no activity in about 11 months (stale) | `comment_and_close` |
| [112](https://github.com/valkey-io/valkey/pull/112) | Use io_uring to batch handle clients pending write… | zhulipeng | merge conflicts; no activity in over 1 year (ancient) | `comment_and_close` |


### Maintainer-flagged to close

| PR | Title | Author | Evidence | Proposed action |
|----|-------|--------|----------|-----------------|
| [3558](https://github.com/valkey-io/valkey/pull/3558) | hash: harden HRANDFIELD against expired-heavy hash… | charsyam | merge conflicts; no activity in about 2 months (cooling) | `review_flagged_close` |
| [3427](https://github.com/valkey-io/valkey/pull/3427) | Windows native builds & tests (Microsoft Visual St… | SamuelMarks | merge conflicts; changes requested, not addressed; no activity in about 2 months (cooling) | `review_flagged_close` |
| [974](https://github.com/valkey-io/valkey/pull/974) | Fix data loss when the old primary takes over the … | enjoy-binbin | merge conflicts; no activity in over 1 year (ancient) | `review_flagged_close` |


## ✍️ Ball in Author's Court

_Waiting on the author (CI red / conflicts / unaddressed review). Longest-idle first._

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [363](https://github.com/valkey-io/valkey/pull/363) | Add support for compiling with mimalloc  | WM0323 | 2.3y |
| [405](https://github.com/valkey-io/valkey/pull/405) | add user-client mapping. | Shuen14 | 2.2y |
| [449](https://github.com/valkey-io/valkey/pull/449) | Batch applying events to kqueue | panjf2000 | 2.2y |
| [690](https://github.com/valkey-io/valkey/pull/690) | Refactor debug configuration options for clarity and consistency | PingXie | 2.1y |
| [599](https://github.com/valkey-io/valkey/pull/599) | Use io_uring to make fsync asynchronous when set appendfsync to always… | zhulipeng | 2.1y |
| [906](https://github.com/valkey-io/valkey/pull/906) | Keep the log fd, don't re-open logfile in every logs | enjoy-binbin | 1.9y |
| [929](https://github.com/valkey-io/valkey/pull/929) | Remove direct reference to conn->fd and use the connection abstraction | naglera | 1.9y |
| [568](https://github.com/valkey-io/valkey/pull/568) | Persistence - Remove Unowned Keys | singku | 2.2y |
| [1407](https://github.com/valkey-io/valkey/pull/1407) | Add tests for src/module examples | Codebells | 1.6y |
| [750](https://github.com/valkey-io/valkey/pull/750) | Persist AOF file by io_uring | Wenwen-Chen | 2.1y |
| [1284](https://github.com/valkey-io/valkey/pull/1284) | fix: readonly client moved inconsistency | proost | 1.7y |
| [1038](https://github.com/valkey-io/valkey/pull/1038) | Add test cases for valkey-benchmark negative path | Shivshankar-Reddy | 1.9y |
| [1120](https://github.com/valkey-io/valkey/pull/1120) | Add admin-port to let administrator connect to the server even maxclie… | hwware | 1.8y |
| [112](https://github.com/valkey-io/valkey/pull/112) | Use io_uring to batch handle clients pending writes to reduce SYSCALL … | zhulipeng | 2.3y |
| [1424](https://github.com/valkey-io/valkey/pull/1424) | Add latency sample for transaction and pipeline | RayaCoo | 1.6y |
| [1547](https://github.com/valkey-io/valkey/pull/1547) | feat: stats and keyspace notifications about lazy expiration | proost | 1.5y |
| [1543](https://github.com/valkey-io/valkey/pull/1543) | Use MSG_ZEROCOPY for plaintext replication traffic | murphyjacob4 | 1.5y |
| [1689](https://github.com/valkey-io/valkey/pull/1689) | Implementation of CPU throttling | lschmidtcavalcante-sc | 1.5y |
| [831](https://github.com/valkey-io/valkey/pull/831) | Add maxmemory-reserved parameter for evicting key earlier to avoid OOM | hwware | 2.0y |
| [1909](https://github.com/valkey-io/valkey/pull/1909) | Add cluster-non-random-gosip option | VyacheslavVanin | 1.3y |
| [1927](https://github.com/valkey-io/valkey/pull/1927) | Mark primary node as alive immediately if reachable and failover is no… | hpatro | 1.3y |
| [1888](https://github.com/valkey-io/valkey/pull/1888) | Change the usec_per_call operation from float to long long division | bluayer | 1.3y |
| [2183](https://github.com/valkey-io/valkey/pull/2183) | Spelling | jsoref | 1.1y |
| [2252](https://github.com/valkey-io/valkey/pull/2252) | Spelling 16 | jsoref | 1.1y |
| [2250](https://github.com/valkey-io/valkey/pull/2250) | Spelling 14 | jsoref | 1.1y |
| [2248](https://github.com/valkey-io/valkey/pull/2248) | spelling: otherwise, | jsoref | 1.1y |
| [2242](https://github.com/valkey-io/valkey/pull/2242) | spelling: cannot | jsoref | 1.1y |
| [2238](https://github.com/valkey-io/valkey/pull/2238) | spelling: ; otherwise, | jsoref | 1.1y |
| [2251](https://github.com/valkey-io/valkey/pull/2251) | spelling: set up | jsoref | 1.1y |
| [2249](https://github.com/valkey-io/valkey/pull/2249) | Spelling 13 | jsoref | 1.1y |
| [2241](https://github.com/valkey-io/valkey/pull/2241) | Spelling 4 | jsoref | 1.1y |
| [2253](https://github.com/valkey-io/valkey/pull/2253) | Spelling 17 | jsoref | 1.1y |
| [2306](https://github.com/valkey-io/valkey/pull/2306) | Unexpected variable overriding from .make-settings file | yzc-yzc | 1.1y |
| [2318](https://github.com/valkey-io/valkey/pull/2318) | change check order for xautoclaim | charsyam | 1.1y |
| [2247](https://github.com/valkey-io/valkey/pull/2247) | spelling: nonexistent | jsoref | 1.1y |
| [2243](https://github.com/valkey-io/valkey/pull/2243) | Spelling 6 | jsoref | 1.1y |
| [2239](https://github.com/valkey-io/valkey/pull/2239) | Spelling 2 | jsoref | 1.1y |
| [2265](https://github.com/valkey-io/valkey/pull/2265) | Implement tunneling support for non-cluster post-failover scenarios | yairgott | 1.1y |
| [2213](https://github.com/valkey-io/valkey/pull/2213) | Optimize bitcount by using AVX-512 intrinsic | shanwan1 | 1.1y |
| [663](https://github.com/valkey-io/valkey/pull/663) | Fix 32-bit atomic linking on powerpc | PingXie | 2.1y |
| [2244](https://github.com/valkey-io/valkey/pull/2244) | Spelling 7 | jsoref | 1.1y |
| [356](https://github.com/valkey-io/valkey/pull/356) | Background Job Manager (BJM) - replacement for BIO | JimB123 | 2.3y |
| [2576](https://github.com/valkey-io/valkey/pull/2576) | bio.c: Split thread function into smaller parts | TedLyngmo | 10mo |
| [2551](https://github.com/valkey-io/valkey/pull/2551) | Roll backward downgrade compatibility from Redis 7.2 and Valkey 7.2/8.… | satheeshaGowda | 11mo |
| [2577](https://github.com/valkey-io/valkey/pull/2577) | bio.c: Split thread function into smaller parts v2 | TedLyngmo | 10mo |
| [2552](https://github.com/valkey-io/valkey/pull/2552) | Multi Threaded RDB Load | Nicky-2000 | 11mo |
| [2496](https://github.com/valkey-io/valkey/pull/2496) | Add static specifier to the internal functions of HLL | yzc-yzc | 11mo |
| [707](https://github.com/valkey-io/valkey/pull/707) | Allow multi-slot MGET in Cluster Mode | JohnSully | 2.1y |
| [2795](https://github.com/valkey-io/valkey/pull/2795) | updated modules examples to compile on Valkey 7.2 branch | dmitrypol | 8mo |
| [2255](https://github.com/valkey-io/valkey/pull/2255) | Accept socket judge fd overflow | kukey | 1.1y |
| [2914](https://github.com/valkey-io/valkey/pull/2914) | Add TLS client presented certificate expiry warnings and KPI | YiwenZhang12 | 7mo |
| [2820](https://github.com/valkey-io/valkey/pull/2820) | Implemented a merge queue for PRs | Nikhil-Manglore | 8mo |
| [2664](https://github.com/valkey-io/valkey/pull/2664) | add_memalign_func | luorong1999 | 9mo |
| [3105](https://github.com/valkey-io/valkey/pull/3105) | SET: add IFNE conditional option | arshidkv12 | 6mo |
| [3153](https://github.com/valkey-io/valkey/pull/3153) | add warning log when certs are expired/not yet valid | YiwenZhang12 | 5mo |
| [3189](https://github.com/valkey-io/valkey/pull/3189) | implement replica-announce-name | bandalgomsu | 5mo |
| [3239](https://github.com/valkey-io/valkey/pull/3239) | Fix SIGTERM crash during Lua script execution | dvkashapov | 5mo |
| [3157](https://github.com/valkey-io/valkey/pull/3157) | Increase valkey-benchmark max latency bucket to 60 seconds | gabiganam | 5mo |
| [3148](https://github.com/valkey-io/valkey/pull/3148) | fix(cluster): Resolve serverAssert(link != sender->link) crash in larg… | liwei330249526 | 5mo |
| [3207](https://github.com/valkey-io/valkey/pull/3207) | Move CONFIG REWRITE disk I/O to background thread | riskywindow | 5mo |
| [2982](https://github.com/valkey-io/valkey/pull/2982) | Add option in valkey-benchmark.c to output result in the file | fluorescentury | 7mo |
| [3305](https://github.com/valkey-io/valkey/pull/3305) | empty kvstore when it has empty allocated hashtables | aradz44 | 4mo |
| [3245](https://github.com/valkey-io/valkey/pull/3245) | Fix assertion crash in processIOThreadsReadDone when DONT_PARSE client… | aradz44 | 5mo |
| [3210](https://github.com/valkey-io/valkey/pull/3210) | tests: make test_entryUpdate allocator-agnostic | seonghoj-bright | 5mo |
| [2976](https://github.com/valkey-io/valkey/pull/2976) | Offload read commands cluster mode enabled | uriyage | 7mo |
| [3268](https://github.com/valkey-io/valkey/pull/3268) | ci: add top-level permissions to remaining workflows | u-wlkjyy | 4mo |
| [866](https://github.com/valkey-io/valkey/pull/866) | New maxmemory-scripts config to limit all cached scripts (EVAL and SCR… | enjoy-binbin | 2.0y |
| [3348](https://github.com/valkey-io/valkey/pull/3348) | Ignore stale readable callbacks after replica sync handoff | sarthakaggarwal97 | 4mo |
| [3269](https://github.com/valkey-io/valkey/pull/3269) | Convert LTTng tracepoints from duration to entry/exit pairs | MatthewKhouzam | 4mo |
| [3302](https://github.com/valkey-io/valkey/pull/3302) | Fix TSAN compatibility for module loading | baswanth09 | 4mo |
| [3383](https://github.com/valkey-io/valkey/pull/3383) | allow to disable dlopen for rdma libs | remicollet | 4mo |
| [3376](https://github.com/valkey-io/valkey/pull/3376) | Fix valkey-benchmark `FUNCTION LOAD` write to replicas (#1846) | hieu2102 | 4mo |
| [3296](https://github.com/valkey-io/valkey/pull/3296) | External data (aka tiered storage?) core with tests | kronwerk | 4mo |
| [2627](https://github.com/valkey-io/valkey/pull/2627) | Skip AOF rewrite when a short write occurs | chenyang8094 | 10mo |
| [3413](https://github.com/valkey-io/valkey/pull/3413) | Optimize infoCommand with SDS pre-allocation | charsyam | 4mo |
| [2989](https://github.com/valkey-io/valkey/pull/2989) | Fix empty shard reconfiguration after CLUSTER RESET SOFT | enjoy-binbin | 6mo |
| [3490](https://github.com/valkey-io/valkey/pull/3490) | Add LCS LEN fast path using rolling two-row DP | charsyam | 3mo |
| [3480](https://github.com/valkey-io/valkey/pull/3480) | Minor optimizations for CLUSTER SHARDS | nmvk | 3mo |
| [3428](https://github.com/valkey-io/valkey/pull/3428) | Improve AGENTS.md with comprehensive development guide | soloestoy | 3mo |
| [3508](https://github.com/valkey-io/valkey/pull/3508) | Fix TLS infinite busy loop when write/read handlers are removed | yairgott | 3mo |
| [3169](https://github.com/valkey-io/valkey/pull/3169) | Support using base aof for full synchronization | cjx-zar | 5mo |
| [3549](https://github.com/valkey-io/valkey/pull/3549) | tls: prevent stale auto-reload from overriding CONFIG SET | charsyam | 3mo |
| [2965](https://github.com/valkey-io/valkey/pull/2965) | Hotkey detection function | li-benson | 7mo |
| [3510](https://github.com/valkey-io/valkey/pull/3510) | Fix TLS infinite busy loop when write/read handlers are removed | yairgott | 3mo |
| [3603](https://github.com/valkey-io/valkey/pull/3603) | Fix: connSocketBlockingConnect ignores aeWait errors (-1) | xdk-amz | 2mo |
| [3468](https://github.com/valkey-io/valkey/pull/3468) | Ignore stale replica messages for failed primaries | sarthakaggarwal97 | 3mo |
| [3705](https://github.com/valkey-io/valkey/pull/3705) | fix: duplicated words in networking/server/function_lua comments | vip892766gma | 2mo |
| [3730](https://github.com/valkey-io/valkey/pull/3730) | conf: document chown(2) requirement for unixsocketgroup | moko-poi | 2mo |
| [3729](https://github.com/valkey-io/valkey/pull/3729) | Fix article/grammar errors in code comments | moko-poi | 2mo |
| [3707](https://github.com/valkey-io/valkey/pull/3707) | Support VALKEYMODULE_REPLY_AGAIN in VM_UnblockClient Reply cb | KarthikSubbarao | 2mo |
| [3502](https://github.com/valkey-io/valkey/pull/3502) | Cache Lua server.call() argv to reduce allocations in hot loops | rjd15372 | 3mo |
| [2555](https://github.com/valkey-io/valkey/pull/2555) | Use BIO thread for cluster config saving in cluster-config-save-behavi… | enjoy-binbin | 11mo |
| [3821](https://github.com/valkey-io/valkey/pull/3821) | Add support for named-databases - HLD | eifrah-aws | 2mo |
| [3605](https://github.com/valkey-io/valkey/pull/3605) | Add SIMD (AVX2 + NEON) acceleration for BITOP AND/OR/XOR/NOT | ihabwahbi | 2mo |
| [2279](https://github.com/valkey-io/valkey/pull/2279) | The smaller config epoch primary will become the replica when two prim… | enjoy-binbin | 1.1y |
| [3854](https://github.com/valkey-io/valkey/pull/3854) | implement `VM_ClusterIsSlotImporting` | bandalgomsu | 8w |
| [3728](https://github.com/valkey-io/valkey/pull/3728) | Fix grammatical typo "This functions" in code comments | moko-poi | 2mo |
| [3907](https://github.com/valkey-io/valkey/pull/3907) | Fork-based Per-type Object Memory Profiling | artikell | 7w |
| [3906](https://github.com/valkey-io/valkey/pull/3906) | fix: improve Makefile robustness by accomodating file paths with space… | mebinthattil | 7w |
| [3894](https://github.com/valkey-io/valkey/pull/3894) | Add connection tunneling feature for Primary failover | omanges | 7w |
| [3539](https://github.com/valkey-io/valkey/pull/3539) | Changes to use word-based bitwise processing for slot updates | omanges | 3mo |
| [3922](https://github.com/valkey-io/valkey/pull/3922) | Harden stream validation on RDB load against crafted metadata | madolson | 7w |
| [3905](https://github.com/valkey-io/valkey/pull/3905) | Optimize .clang-format and add enum/argument formatting options | harrylin98 | 7w |
| [3534](https://github.com/valkey-io/valkey/pull/3534) | string: avoid storing already-expired MSETEX values | charsyam | 3mo |
| [3956](https://github.com/valkey-io/valkey/pull/3956) | Fix garbage earliest-expiry read in vsetEstimatedEarliestExpiry RAX pa… | ranshid | 6w |
| [3976](https://github.com/valkey-io/valkey/pull/3976) | Fix reserved identifier violations in include guards (#3850) | vansvan17 | 6w |
| [3973](https://github.com/valkey-io/valkey/pull/3973) | Clear import-source flag on connection state reset | tjade273 | 6w |
| [3972](https://github.com/valkey-io/valkey/pull/3972) | Validate PUBLISH and MODULE payload lengths against packet size | tjade273 | 6w |
| [3971](https://github.com/valkey-io/valkey/pull/3971) | Fix GEORADIUS STORE ACL bypass via duplicate options | tjade273 | 6w |
| [3799](https://github.com/valkey-io/valkey/pull/3799) | Fix deadlock in pipelined ingestion when command spans TCP packet boun… | alon-arenberg | 2mo |
| [3991](https://github.com/valkey-io/valkey/pull/3991) | Parse the server INFO buffer in place in VM_GetServerInfo | jjuleslasarte | 5w |
| [2180](https://github.com/valkey-io/valkey/pull/2180) | Hash prefetching | xbasel | 1.1y |
| [3648](https://github.com/valkey-io/valkey/pull/3648) | Forkless Snapshot (Threadsave) | nitaicaro | 2mo |
| [4010](https://github.com/valkey-io/valkey/pull/4010) | Limit multibulk args count and fix integer type truncations | wufengwind | 5w |
| [3389](https://github.com/valkey-io/valkey/pull/3389) | Optimize multi key commands (such as MGET, MSET, DEL, UNLINK, EXISTS a… | satheeshaGowda | 4mo |
| [3363](https://github.com/valkey-io/valkey/pull/3363) | Defer command execution during long-running scripts | amanosme | 4mo |
| [3611](https://github.com/valkey-io/valkey/pull/3611) | Fix RDMA + IO threads re-entrancy and busy-loop via connection postpon… | quanyeyang | 2mo |
| [3589](https://github.com/valkey-io/valkey/pull/3589) | ci: Add slow tag to fuzzer and expand libc-malloc CI to run tests | jjuleslasarte | 2mo |
| [4056](https://github.com/valkey-io/valkey/pull/4056) | Rename reserved-identifier header guards to the NAME_H convention | AlisinaDevelo | 4w |
| [3833](https://github.com/valkey-io/valkey/pull/3833) | Speed up split-vote elections with the new FAILOVER_AUTH_NACK message | enjoy-binbin | 2mo |
| [4054](https://github.com/valkey-io/valkey/pull/4054) | Reject bare "(" and empty string in zset score ranges | AlisinaDevelo | 4w |
| [4061](https://github.com/valkey-io/valkey/pull/4061) | ACL: Check aclfile writability before ACL SAVE | lcxn123 | 4w |
| [4075](https://github.com/valkey-io/valkey/pull/4075) | Streaming Compression support for fullsync | roshkhatri | 3w |
| [4025](https://github.com/valkey-io/valkey/pull/4025) | tests/rdma: add libvalkey pipeline regression test for RDMA + IO threa… | quanyeyang | 4w |
| [3853](https://github.com/valkey-io/valkey/pull/3853) | Streaming Compression support for Replication | roshkhatri | 8w |
| [3717](https://github.com/valkey-io/valkey/pull/3717) | Add support for secondary certificates | pkhartsk | 2mo |
| [3459](https://github.com/valkey-io/valkey/pull/3459) | Fix missing signalModifiedKey calls for stream commands | Tarte12 | 3mo |
| [4003](https://github.com/valkey-io/valkey/pull/4003) | Add futex-based blocking when main thread waits for IO poll results | asafpamzn | 5w |
| [4052](https://github.com/valkey-io/valkey/pull/4052) | Require a [release-notes] or [no-release-notes] label on PRs | BChan-0 | 4w |
| [4015](https://github.com/valkey-io/valkey/pull/4015) | Raft Cluster: stability fixes | zuiderkwast | 4w |
| [4094](https://github.com/valkey-io/valkey/pull/4094) | Raft Cluster: Implement Non-voting Members | quanyeyang | 3w |
| [4079](https://github.com/valkey-io/valkey/pull/4079) | Route INFO generation (core + module API) through a pluggable info emi… | omerrubi-amzn | 3w |
| [4017](https://github.com/valkey-io/valkey/pull/4017) | Optimize HMGET, SMISMEMBER and ZMSCORE with batched hashtable lookup | chzhoo | 4w |
| [3651](https://github.com/valkey-io/valkey/pull/3651) | info: add command breakdown to Errorstats | servusdei2018 | 2mo |
| [4122](https://github.com/valkey-io/valkey/pull/4122) | Fixes RESP response splitting in the Lua shebang error path. | localhost-detect | 2w |
| [4121](https://github.com/valkey-io/valkey/pull/4121) | Fix bitfield command did not replicate when only creating or resizing | cjx-zar | 2w |
| [4118](https://github.com/valkey-io/valkey/pull/4118) | perf: Drop redundant per-command peak-memory sampling in `call()` | rainsupreme | 2w |
| [4110](https://github.com/valkey-io/valkey/pull/4110) | Remove per-iteration overhead from the IO thread main loop | omerrubi-amzn | 2w |
| [4109](https://github.com/valkey-io/valkey/pull/4109) | Coalesce small bulk replies into a single buffer append | omerrubi-amzn | 2w |
| [4108](https://github.com/valkey-io/valkey/pull/4108) | Skip commandlog bookkeeping when no threshold is crossed | omerrubi-amzn | 2w |
| [4107](https://github.com/valkey-io/valkey/pull/4107) | Fix false sharing in per-thread memory usage counters | omerrubi-amzn | 2w |
| [4007](https://github.com/valkey-io/valkey/pull/4007) | Randomize hashtable scan start to avoid cursor=0 restart bias | hpatro | 5w |
| [3924](https://github.com/valkey-io/valkey/pull/3924) | valkey-cli: avoid MULTI/EXEC for cluster fix on Raft clusters | quanyeyang | 7w |
| [4129](https://github.com/valkey-io/valkey/pull/4129) | Fix out-of-bounds read in vsnprintf_async_signal_safe on a trailing '%… | magic-peach | 2w |
| [4083](https://github.com/valkey-io/valkey/pull/4083) | Implement transfer leadership before forgetting the current leader | bandalgomsu | 3w |
| [4146](https://github.com/valkey-io/valkey/pull/4146) | Fix XSETID ENTRIESADDED error message to include the accepted value 0 | nikolauspschuetz | 2w |
| [4140](https://github.com/valkey-io/valkey/pull/4140) | Retry PSYNC on -BUSY error instead of downgrading to SYNC | enjoy-binbin | 2w |
| [4093](https://github.com/valkey-io/valkey/pull/4093) | Emit latency metrics for round trip time for cluster nodes | ydsakshi | 3w |
| [4155](https://github.com/valkey-io/valkey/pull/4155) | Fix MOVE/COPY command skip the current-DB ACL check | cjx-zar | 12d |
| [4163](https://github.com/valkey-io/valkey/pull/4163) | Solution (#4143): [BUG] Tracking table items not cleaned after client … | TFGSUMIT | 11d |
| [3335](https://github.com/valkey-io/valkey/pull/3335) | Fix RDMA re-entrancy assertion and lost wakeup deadlocks with I/O thre… | quanyeyang | 4mo |
| [4160](https://github.com/valkey-io/valkey/pull/4160) | Fix out-of-memory DoS on HRANDFIELD, ZRANDMEMBER and SRANDMEMBER with … | warrenzhu25 | 12d |
| [4147](https://github.com/valkey-io/valkey/pull/4147) | fix: remove duplicated words and correct grammar in comments | magic-peach | 2w |
| [4190](https://github.com/valkey-io/valkey/pull/4190) | Reclaim dead client IDs from the tracking table (#4143) | rayjinghaolei | 10d |
| [4184](https://github.com/valkey-io/valkey/pull/4184) | Say non-negative in the shared positive-count range error message | AlisinaDevelo | 10d |
| [4214](https://github.com/valkey-io/valkey/pull/4214) | fix(acl): prevent NULL pointer dereference on malformed selector in AC… | magic-peach | 6d |
| [4213](https://github.com/valkey-io/valkey/pull/4213) | fix(debug): add bounds check in memtest_test_linux_anonymous_maps to p… | magic-peach | 6d |
| [4211](https://github.com/valkey-io/valkey/pull/4211) | Prevent double-free of the module timer when the callback stops it | quanyeyang | 7d |
| [4201](https://github.com/valkey-io/valkey/pull/4201) | Add CRC32 integrity check for cluster bus messages | enjoy-binbin | 8d |
| [4171](https://github.com/valkey-io/valkey/pull/4171) | Fix ping_sent getting stuck when peer traffic keeps link alive | enjoy-binbin | 10d |
| [4232](https://github.com/valkey-io/valkey/pull/4232) | Bump minimum cmake version to 3.24 | Baraa-Hasheesh | 4d |
| [4161](https://github.com/valkey-io/valkey/pull/4161) | Optimize exact XTRIM MAXLEN zero | sarthakaggarwal97 | 12d |
| [2470](https://github.com/valkey-io/valkey/pull/2470) | Multi threaded RDB Save | Nicky-2000 | 11mo |
| [2375](https://github.com/valkey-io/valkey/pull/2375) | config option to stop master on AOF write error | kronwerk | 1.0y |
| [3984](https://github.com/valkey-io/valkey/pull/3984) | AOF loading must not check ACL permissions in exec | lukepalmer | 6w |
| [3940](https://github.com/valkey-io/valkey/pull/3940) | Nested prefetching for hash and zset inner hashtables | roshkhatri | 6w |
| [4256](https://github.com/valkey-io/valkey/pull/4256) | Parallelize Valgrind tests to reduce Daily Runtime | sarthakaggarwal97 | 3d |
| [4254](https://github.com/valkey-io/valkey/pull/4254) | Convert oversized hash listpacks during RDB load | ANSHUL-REAL | 4d |
| [4215](https://github.com/valkey-io/valkey/pull/4215) | valkey-benchmark: reject empty command sequence instead of hanging | dhruv2x | 6d |
| [4262](https://github.com/valkey-io/valkey/pull/4262) | Also free string object under THP in fork child | enjoy-binbin | 2d |
| [4251](https://github.com/valkey-io/valkey/pull/4251) | deflake ccov: Use _exit() when a child is killed by SIGUSR1 | rainsupreme | 4d |
| [4127](https://github.com/valkey-io/valkey/pull/4127) | Cluster Bus v2 -  Decentralized Failure Detector | sushilpaneru1 | 2w |
| [4076](https://github.com/valkey-io/valkey/pull/4076) | QoS for system critical events ( such as cluster heartbeats, replicati… | satheeshaGowda | 3w |
| [4005](https://github.com/valkey-io/valkey/pull/4005) | Reserve connection slots for priority sources | satheeshaGowda | 5w |
| [3677](https://github.com/valkey-io/valkey/pull/3677) | fix json.mset first win, revert #2365 | cjx-zar | 2mo |
| [4272](https://github.com/valkey-io/valkey/pull/4272) | Fix slow-clocksource advisory for non-x86 | quanyeyang | 0d |
| [4270](https://github.com/valkey-io/valkey/pull/4270) | make getMonotonicUs static in libvalkeylua | mohammedgqudah | 0d |

---

*Report generated by [valkey-pr-watchtower](https://github.com/valkey-rainfall/valkey-pr-watchtower). Data from GitHub API. Opinions are the author's own.*