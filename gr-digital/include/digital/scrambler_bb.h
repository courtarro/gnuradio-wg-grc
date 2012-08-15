/* -*- c++ -*- */
/*
 * Copyright 2008,2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_GR_SCRAMBLER_BB_H
#define INCLUDED_GR_SCRAMBLER_BB_H

#include <digital/api.h>
#include <gr_sync_block.h>

namespace gr {
  namespace digital {

    /*!
     * Scramble an input stream using an LFSR.  This block works on
     * the LSB only of the input data stream, i.e., on an "unpacked
     * binary" stream, and produces the same format on its output.
     *
     * \param mask     Polynomial mask for LFSR
     * \param seed     Initial shift register contents
     * \param len      Shift register length
     *
     * \ingroup coding_blk
     */

    class DIGITAL_API scrambler_bb : virtual public gr_sync_block
    {
    public:
      // gr::digital::scrambler_bb::sptr
      typedef boost::shared_ptr<scrambler_bb> sptr;

      static sptr make(int mask, int seed, int len);
    };

  } /* namespace digital */
} /* namespace gr */

#endif /* INCLUDED_GR_SCRAMBLER_BB_H */