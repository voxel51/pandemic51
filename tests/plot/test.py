'''

'''
import eta.core.serial as etas

import pandemic51.core.database as pand


stream_name = "time_square"

output_result = pand.query_stream_pdi(stream_name)


d = {
    "time": [a["time"] for a in output_result],
    "pdi": [a["pdi"] for a in output_result]
}

etas.write_json(d, "test.json")
